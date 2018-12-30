import pandas as pd
import re

from sklearn.preprocessing import OneHotEncoder


p_caps = re.compile(r'@caps\d{0,2}', re.I)
p_city = re.compile(r'@city\d{0,2}', re.I)
p_date = re.compile(r'@date\d{0,2}', re.I)
p_dr = re.compile(r'@dr\d{0,2}', re.I)
p_location = re.compile(r'@location\d{0,2}', re.I)
p_money = re.compile(r'@money\d{0,2}', re.I)
p_month = re.compile(r'@month\d{0,2}', re.I)
p_num = re.compile(r'@num\d{0,2}', re.I)
p_organization = re.compile(r'@organization\d{0,2}', re.I)
p_percent = re.compile(r'@percent\d{0,2}', re.I)
p_person = re.compile(r'@person\d{0,2}', re.I)
p_state = re.compile(r'@state\d{0,2}', re.I)
p_time = re.compile(r'@time\d{0,2}', re.I)
p_email = re.compile(r'@email\d{0,2}', re.I)


type_mapping = {
    0: 'persuasive_narrative_expository',
    1: 'source dependent responses'
}






def replace_label(e):
    p_caps = re.compile(r'@caps\d{0,2}', re.I)
    p_city = re.compile(r'@city\d{0,2}', re.I)
    p_date = re.compile(r'@date\d{0,2}', re.I)
    p_dr = re.compile(r'@dr\d{0,2}', re.I)
    p_location = re.compile(r'@location\d{0,2}', re.I)
    p_money = re.compile(r'@money\d{0,2}', re.I)
    p_month = re.compile(r'@month\d{0,2}', re.I)
    p_num = re.compile(r'@num\d{0,2}', re.I)
    p_organization = re.compile(r'@organization\d{0,2}', re.I)
    p_percent = re.compile(r'@percent\d{0,2}', re.I)
    p_person = re.compile(r'@person\d{0,2}', re.I)
    p_state = re.compile(r'@state\d{0,2}', re.I)
    p_time = re.compile(r'@time\d{0,2}', re.I)
    p_email = re.compile(r'@email\d{0,2}', re.I)

    text = e
    text = p_caps.sub('LABEL_CAPS', text)
    text = p_city.sub('LABEL_CITY', text)
    text = p_date.sub('LABEL_DATE', text)

    text = p_dr.sub('LABEL_DR', text)
    text = p_location.sub('LABEL_LOCATION', text)
    text = p_money.sub('LABEL_MONEY', text)
    text = p_month.sub('LABEL_MONTH', text)
    text = p_num.sub('LABEL_NUM', text)
    text = p_organization.sub('LABEL_ORGANIZATION', text)
    text = p_percent.sub('LABEL_PERCENT', text)
    text = p_person.sub('LABEL_PERSON', text)
    text = p_state.sub('LABEL_STATE', text)
    text = p_time.sub('LABEL_TIME', text)
    text = p_email.sub('LABEL_EMAIL', text)
    return text


def cleaning_raw_data(filename):
    df = pd.read_csv(filename)
    df['essay_clean'] = df.essay.apply(replace_label)

    df['type_of_essay'] = df['type_of_essay'].str.replace(
        'persuasive / narrative  / expository', '0', case=True, regex=False)

    df['type_of_essay'] = df['type_of_essay'].str.replace(
        'source dependent responses', '1', case=True, regex=False)

    df['type_of_essay'] = df['type_of_essay'].astype(int)

    # df_level = pd.get_dummies(df['grade_level'], prefix='level')




cleaning_raw_data('training.csv')