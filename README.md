# RNN based Automated Essay Grading System
The previous or existing automated essay grading systems used traditional text based machine learning models. The results highly rely on the crafted extracted features. The performances are unstable when grading different essays from various topics. 

I propose a deep learning based (recurrent neural networks) method to grading essays automatically without any feature engineering. By training multiple recurrent neural networks models, the system can perform a better result compare to traditional methods. 

The system designed to be user-friendly, after input the required selection and paste the essay in text-box, the scoring will show up with three optional different scoring ranges.

### Dataset
All datasets can be found on Kaggle :  https://www.kaggle.com/c/asap-aes/data/

### Recurrent Neural Networks
Since we treat the textual data as a single vector, a regular single feed-forwarding neural network might not perform very well. Such a model actually doesn’t have any memory of any previous ingested data point. Each data point processed independently and no relationships. This is not a good way to automated grading essays. Plus the order of words is very important.
Recurrent neural networks can behave somehow like a human when reading a text by iterating through each word and considering all relative information from previous. In practice, if we implement an internal loop and feeding the previous element into current layer, each step will be viewed by the next layer.
<br>
<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-08%20at%2010.21.23%20PM.png" width="300">

In theory, each h holds all information from previous timestamps. However, in practice, the model couldn’t handle the long essays since the distance is too far away. This issue is referred as the vanishing gradient problem. Basically, this problem occurs because the neural network propagated over so many layers and the information tends to vanish. Instead of holding all words, the solution is using long short-term memory network. The LSTM actually computed by setup some gate architectures.
<br>
<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-08%20at%2010.37.51%20PM.png" width="300">

In above figure, it shows how the LSTM takes steps to create new state using the old state and current input. LSTM splits the state vector into two components: state component h and memory component c. Other gates referred to input gate i, forget gate f, output gate o. The forget gate decides how much of previous memory should be used in the computation. The input gate determines how much input x and previous state should be preserved. The new memory cell c is produced by using the results from three other gates. Finally, the new state created.
LSTM can help us to produce a better result from the sequential textual data and skip the problem of vanishing gradient. A regular recurrent neural network model does not change the interpretation of previous words. But as human, we constantly changing the interpretation based on the next sentence. One of the goals is also to make our automated essay grading system can grading essays like a human: reading essays and understanding it.


### Model Parameters
- The number of epoch: 100
- Batch size: 2048
- Validation and testing percentage: 0.2
- Function used for avoid over-fitting: dropout
- Activation function: sigmoid function
- Loss function: cross-entropy loss and mean square error quadratic loss.
- Optimize function: adam
- Result measurement: mean absolute error

### Performances
<br>
<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-09%20at%203.22.08%20PM.png" width="350">
<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-09%20at%203.22.18%20PM.png" width="350">

Above figures extracted from two neural networks without the embedding layer. The left neural network includes the input parameters (grade level, essay type) and the right neural network without input parameters. Both figures show that the loss is getting less and less over 100 epochs but the validation error is getting larger and larger, the model is over-fitting.

Below figures extracted from two neural networks with the embedding layer. The left neural network includes the input parameters (grade level, essay type) and the right neural network without input parameters. Both figures show a similar trend over time. With more and more training data and over 100 epochs, this model should perform better and better without over-fitting.
<br>
<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-09%20at%203.21.36%20PM.png" width="350">
<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-09%20at%203.21.59%20PM.png" width="350">

### Data Flow Architecture
After the user pasted their essay in text box and selected the correspondent information. The text essay data and parameters will be delivered to the server side (model side). The submit button will trigger the main function. Since the raw data has noise. The pre-processing section will clean up the essay with a better format and pass essay into a pre-trained model, the model will fit the input text data and return a numeric result as a predicted score. At each time, except return score as result, this system will also copy the essay into a document-oriented database and update current model. Other analysis can be performed at this phase from output file.
To improve the computing efficiently, the training process will only occur by a manually commend, but existing model parameters can always provide a predicted score.

<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-08%20at%205.51.25%20PM.png" width="300">

### User Page
The user interface was designed to be clean and concise. The grade level will also be counted as the input data and fit into the deep learning model, ideally, the same essay should get different scores with different grade level as input. The result of essay grading will be a numeric score between 0 and 1. This result can be converted into different range like zero to ten or zero to one hundred. The final score should show up in the score box with less than one second response time after the user pastes their essay into an essay input box.

<img src="https://github.com/yetianpro/automated-essay-grading-by-RNN/blob/master/figures/Screen%20Shot%202018-12-08%20at%204.21.53%20PM.png" width="500">




