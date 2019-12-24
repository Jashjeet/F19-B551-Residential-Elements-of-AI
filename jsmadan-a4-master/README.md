# a4
## K Nearest Neighbor Classifier
We first read the training and testing files in a pandas data frame. The name and index columns( unique to every row so doesn’t contribute anything to the classification ) and thus are dropped from the data frame. We convert training and testing data frames to numpy arrays. 
We used pandas built-in function get_dummies to convert categorical data to binary data(0,1). It expands the columns of y into the number of unique classes and assigns 1 to the class to which the data point belongs and 0 to all the other columns.

After repeated trial and error we settled for K = 10. We use the square of the Euclidean distance by taking the difference between training data and testing data dimension wise, square each dimension difference and add it to get the resultant square of Euclidean distance. Then we chose the K points with a minimum Euclidean distance by sorting in ascending order and taking first K values. Then we get the select the label of the most frequent class among the K nearest neighbors of the point and label it that class.

After predicting labels for all the testing data we compare the number of values for which the predicted values are equal to the true values and we divide it by the total number of testing values to get the testing accuracy.

The maximum accuracy achieved using KNN on the current testing data using the training data is 71%.

This can be visualized by drawing a circle, and gradually increasing its radius to get the k nearest neighbors. If the K in K Nearest Neighbors is equal to 1, then we are using just the nearest neighbor to classify that datapoint. It will belong to the class of that neighbor. If the K in K Nearest Neighbors is equal to 100, and there is more than 1 category of the nearest neighbors, then we simply pick the category that gets the most votes (the most number of times appearing class).

## Neural Network

In the neural network first, we define learning rate, epochs and a decaying constant for making adaptive learning rate.

Compute function takes the dot product of input with weights and adds bias to it.

### Cross-Entropy Loss Function
Log of the predicted labels is taken along with handling the exception of extremely low probability. Thereafter it is multiplied with the true probability elementwise. The sum of all the terms gives the total loss. For all the elements in a row, the one with the maximum probability is chosen to be 1 while all the others are replaced with 0.
The derivative of the cross-entropy loss function is calculated using the difference between predicted and true values.

### Fit function.
The weights for all the 3 layers in our neural network are initialized using a random function and all the biases are set to 0. The dropout is set to 0.2. We set the number of iterations by dividing the total variables by its step size. We select the number of rows as per the step size for each iteration. Then we call the compute function for the batch size followed by a Relu activation. Then we keep the use of a random function to select 1 - dropout percentage of variables from the complete list( using boolean and then applying that on the predicted variables ) and scale it accordingly. We repeat the same procedure for the second layer. For the final step, we use the compute function followed by a softmax. Then we calculate the loss function. 

### Predict Function.
We use the weights and biases of all the layers to predict output to be fed to the next layer as input. After calculating the final output we compare the number of predicted values matching the true values diving by the number of test cases to get the accuracy of the model.

After defining all the functions, we call the main function and show the accuracy of the model.The maximum accuracy achieved using Neural Network on the current testing data using the training data is 48%.


### Activation Function (Relu).
To transform out linear datapoints to non linear points in a transformed space, we have used Relu as out activation function in the two hidden layers. ReLU stands for Rectified Linear units. It’s just R(x) = max(0,x) i.e if x < 0 , R(x) = 0 and if x >= 0 , R(x) = x. Relu Activation function is used which replaces all values less than 0 by 0 and the values greater than and equal to 0 remain as it is.

### Activation Function Derivative of Relu.
The derivative of ReLU is: f′(x)={1,if x>0 and 0,otherwise(x<=0). It gives 0 value for all the negative and zero values and for 1 for all the positive values.


### Activation Function (Softmax).
Softmax function normalizes the output into probabilities that sum to one (since, the summation of a datapoint belonging to every class will be equal to one). Softmax function outputs a vector that represents the probability distributions of a list of potential outcomes. This vector is equal to the exponentials of the input numbers divided by the sum of the exponentials of the input numbers of that row. After this, the maximum probable class is given 1 and the rest of the classes as 0. We have used mean and the standard deviation to normalize the data.

### Dropout.
To avoid overfitting in machine learning models, different regularization technique are implemented. One such technique in Neural Networks is droupout. As the dataset provided had aroung 36,000 samples, and hidden layers had 512 neurons, this model can easily overfit data and remember every output. In dropout, we create a masking layer, and define dropout probability, i.e. the probability of randomly killing output from a neuron, so that it does not propagate to next level. Keep probability is defined as 1-dropout probability.


### RMSProp.
Root Mean Square Prop is a method to tweak learning rate at every epoch. It takes into consideration the previous scaling factors, decay constant, training loss, derivative of the loss function gradient and adapt learning rate by dividing by the root of gradient. It is a stochastic gradient descent and is performed with minibatches. In this, we have taken minibatches of 5000. So, we get around 50% accuracy in just 5 epochs, as compared to running it for 25 epochs for full batch gradient descent. There is decaying of learning rate and that is defined by rho.



## DECISION TREE
### TRAINING
While building a decision tree, we calculate the mean of all the rows for each column. 
We calculate the expectation which is 4.0 for the current dataset. Since there are only 4 classes and all or of equal frequency so the probability of occurrence of each of them is equal to one quarter. So we get the resultant sum of - p * log2(p) sum for all the 4 classes is 2.
For each column, we iterate through all the rows and classify each value as “>=” for being greater than the mean value and “<” for being less than the mean. Then we get entropy for “>=” for all the 4 classes( 0,90,180,270 ) using the count of each class divided by the total number of counts for all the 4 classes as its probability and then applying summation of - p * log2(p) for all the 4 classes. Similarly, we calculate the entropy for the “<” class. After calculating the entropy for the “>=” and “<” we use expectation - Entropy for “>=” and the “<” separately to calculate the information gain for each of the classes. Then we sum up the information gain for both the classes to get the resultant information gain. The column with maximum information gain is chosen.
At each step, we append a tuple to ( depth, column index, the mean value of the column ). After that, we split the training array into 2 parts based on the fact whether its column value at that particular index is “>=” or “<” and split its respective labels( angles ) respectively. So, on training these two sets of training arrays and labels separately calculate recursion. After which the two arrays are merged back in order to get the old resultant array if needed.
### STOPPING CONDITION
Whenever the training model increased the depth of 3, we stored the label of the majority class in that split and use that as a classification criterion.
So after completing training, we got 2 arrays one with a set of tuples of ( depth, index, mean value ) and the other the array of possible labels in order of split.

### TESTING
While testing through the rows, if the depth of the model is equal to maximum depth then we compare it to the mean value if its “>=” then we equate it to the label of the current index else ( index + 1 ) value of the label. And we exit the loop for that row.
Else we check. If the current row’s index value is “>=” we continue iterating. Else we check the second value whose depth is equal to current depth + 1 since the first value which comes at the current depth will be for “>=” but we want “<” which will be a second value which comes in the array. During this process, we skip 2 ^ ( max depth - current depth ) in the labels( since it has all the values in the respective order ) and thus we add that to the index value. Then we continue 
iterating through the loop for the same.

After generating labels for all the rows, we compare the number of matching labels of the predicted labels with the true labels and we get the testing accuracy.

The maximum accuracy achieved using Decision Tree on the current testing data using the training data is 60%.

For our case the KNN algorithm performs the best among all the 3 algorithms.
