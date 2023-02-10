# BScThesis Jorit Prins
Student nr = 12862789

The use of Machine Learning (ML) typically consists of two phases: training and inference. The training phase is an tedious and time exhausting process. In Machine Learning as a Service, a company or other party offers a pre-trained Neural Network (NN) to the client. MLaaS can offer privacy threats for both the client and the server. Secure Neural Network Inference (SNNI) entails the problem of a client learning the output of a NN held by a server, without the server learning the input and the client about the NN. No approach has been widely accepted, but some proof of concept approaches have been suggested. These approaches are only tested on accuracy and efficiency, while other metrics, like energy consumption are not tested, although they are still of importance. In this thesis, I test how much energy Cheetah consumes compared to its counterpart CrypTFlow2, two of the most recent approaches, and how the bandwidth influences the energy consumption. In this research, I found that there are not many approaches to measure the energy consumption of programs. I did find Scaphandre, and used it to measure the power consumption of Cheetah and CrypTFlow2. I found that Cheetah is not only faster, but also used less power compared to CrypTFlow2. Additionally, I found that the improvement increases when limiting the bandwidth of the client. Energy consumption increases after a certain turn-point.

## Repo Directory Description
- `General documents/` Contains general documents, personal logs and notes.
- `Project plan/` Contains the latex files for the project plan
- `Relevant documents/` Contains relevant documents for this thesis
- `Scaphandre/` Contains the Scaphandre source files
- `Thesis` Contains the latex files for the thesis documents

