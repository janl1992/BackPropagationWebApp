import matplotlib; matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass

learningrate=0.001
# learningrate = 1.6
# filter = 0.8

@dataclass
class Example:
    x: []
    y: []
    def __init__(self, x, y):
        self.x = x
        self.y = y

def initanimation():
    line.set_data(animationarrayfinal[0].x, animationarrayfinal[0].y)
    return line

def update(i):
    # line.set_ydata(np.asarray(animationarrayfinal[i]))
    if i < len(animationarrayfinal):
        line.set_data( animationarrayfinal[i].x, animationarrayfinal[i].y)
        line2.set_UVC( animationweightvectorw1[i][0], animationweightvectorw1[i][1])
        line3.set_UVC( animationweightvectorw0[i][0], animationweightvectorw0[i][1])
    # line.set_data(animationarrayreference[i].x, animationarrayreference[i].y)
    return line, line2, line3

# Reference function on interval -2 <= x <= 2
def referencefunction(x):
    return 1 + np.sin(np.pi / 4 * x)


def purelin(x):
    return x


def purelin1():
    return 1


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid1(x):
    return (np.exp(-x)) / ((1 + np.exp(-x)) ** 2)


def initializeweightandbias():
    global b0, b1, w0, w1, animationweightvectorw0, animationweightvectorw1, animationweightvectorfrontendw0, animationweightvectorfrontendw1
    animationweightvectorw0 = []
    animationweightvectorw1 = []
    animationweightvectorfrontendw0 = []
    animationweightvectorfrontendw1 = []
    maxValueAnimationArray1 = 0
    minValueAnimationArray1 = 0
    # global  = []

    b0 = np.array([-0.08, -0.15])
    b1 = 0.3
    # w0 = np.array([0.5, 1.9])
    # w1 = np.array([0.5, 2.5])
    # b0 = np.array([-3, -3])
    # b1 = 0.3
    # w0 = np.array([-40, -40])
    # w1 = np.array([-40, -40])
    w0 = np.array([-10, -10])
    w1 = np.array([-10, -10])
    animationweightvectorw0.append(w0)
    animationweightvectorw1.append(w1)

def neuralnetwork(xvalue, adjustweight):
    global element, w0, w1, b0, b1
    dot1 = np.dot(xvalue, w0)
    intermediatelayer0 = dot1 + b0
    intermediatelayer0 = np.squeeze(np.asarray(intermediatelayer0))
    intermediatelayeroutput0 = []
    for element in intermediatelayer0:
        intermediatelayeroutput0.append(sigmoid(element))
    intermediatelayer1 = b1 + np.dot(intermediatelayeroutput0, w1)
    intermediatelayeroutput1 = purelin(intermediatelayer1)
    if adjustweight == 1:
        adjustweights(xvalue, referencefunction(xvalue), intermediatelayeroutput0, intermediatelayeroutput1)
    elif adjustweight == 2:
        adjustweightswithfilter(xvalue, referencefunction(xvalue), intermediatelayeroutput0, intermediatelayeroutput1)
    else:
        return intermediatelayeroutput1


def adjustweights(xvalue, yvalue, intermediatelayeroutput0, intermediatelayeroutput1):
    global w0, w1, b0, b1
    error = yvalue - intermediatelayeroutput1
    errorarray.append(error)
    s1 = -2 * purelin1() * (yvalue - intermediatelayeroutput1)
    s0 = np.dot(np.matrix([[sigmoid1(intermediatelayeroutput0[0]), 0], [0, sigmoid1(intermediatelayeroutput0[1])]]),
                np.dot(w1, s1))
    # Adjust weights
    w0 = w0 - learningrate * np.dot(s0, xvalue)
    animationweightvectorw0.append(np.asarray(w0).flatten())
    animationweightvectorfrontendw0.append(Example(np.asarray(w0).flatten()[0], np.asarray(w0).flatten()[1]))
    w1 = w1 - learningrate * np.dot(s1, intermediatelayeroutput0)
    animationweightvectorfrontendw1.append(Example(np.asarray(w1).flatten()[0], np.asarray(w0).flatten()[1]))
    animationweightvectorw1.append(w1)
    b0 = b0 - learningrate * s0
    b1 = b1 - learningrate * s1
    # maxValueAnimationArray1 = np.amax(animationweightvectorw1)
    # minValueAnimationArray1 = np.amin(animationweightvectorw1)

def adjustweightswithfilter(xvalue, yvalue, intermediatelayeroutput0, intermediatelayeroutput1):
    global w0, w1, b0, b1
    error = yvalue - intermediatelayeroutput1
    errorarray.append(error)
    s1 = -2 * purelin1() * (yvalue - intermediatelayeroutput1)
    s0 = np.dot(np.matrix([[sigmoid1(intermediatelayeroutput0[0]), 0], [0, sigmoid1(intermediatelayeroutput0[1])]]),
                np.dot(w1, s1))
    # Adjust weights
    w0 = filter * w0 - ((1 - filter) * learningrate * np.dot(s0, xvalue))
    animationweightvectorw0.append(np.asarray(w0).flatten())
    w1 = filter * w1 - ((1 - filter) * learningrate * np.dot(s1, intermediatelayeroutput0))
    animationweightvectorw1.append(w1)
    b0 = filter * b0 - ((1 - filter) * learningrate * s0)
    b1 = filter * b1 - ((1 - filter) * learningrate * s1)
    # maxValueAnimationArray1 = np.amax(animationweightvectorw1)
    # minValueAnimationArray1 = np.amin(animationweightvectorw1)

def init():
    global yValuesPlotInitial, element
    yValuesPlotInitial = []
    for element in xFinalTrainingArray:
        yValuesInitial = neuralnetwork(element, 0)
        yValuesPlotInitial.append(yValuesInitial)


def prepareTrainingValues():
    global xFinalTrainingArray, element, exampleset
    xTrainingValues = np.arange(-2, 2, 0.1)
    xValidationValues = xTrainingValues[1:-1:4]
    xFinalTrainingArray = []
    isinValidationset = False
    for element in xTrainingValues:
        for element1 in xValidationValues:
            if element == element1:
                isinValidationset = True
                break
        if (isinValidationset != True):
            xFinalTrainingArray.append(element)
        isinValidationset = False
    xArray = np.linspace(0, len(xTrainingValues), len(xTrainingValues), dtype=np.intc)
    exampleset = []
    for element in xFinalTrainingArray:
        exampleset.append(Example(element, referencefunction(element)))

def initialAnimationArray():
    global timesTrainingSetIsPresented, errorarray, animationarrayintermediateY, animationarrayintermediateX, animationarrayreferenceY, animationarrayreferenceX, animationarrayreference, animationarrayfinal
    timesTrainingSetIsPresented = np.arange(0, 100, 1)
    errorarray = []
    animationarrayintermediateY = []
    animationarrayintermediateX = []
    animationarrayreferenceY = []
    animationarrayreferenceX = []
    animationarrayreference = []
    animationarrayfinal = []

def trainNetwork():
    global element, animationarrayintermediateY, animationarrayintermediateX, animationarrayreferenceX, animationarrayreferenceY, yArray
    for element in timesTrainingSetIsPresented:
        for trainingexample in exampleset:
            neuralnetwork(trainingexample.x, 1)
            animationarrayintermediateY.append(neuralnetwork(trainingexample.x, 0))
            animationarrayintermediateX.append(trainingexample.x)
            animationarrayreferenceX.append(trainingexample.x)
            animationarrayreferenceY.append(referencefunction(trainingexample.x))
        animationarrayfinal.append(Example(animationarrayintermediateX, animationarrayintermediateY))
        animationarrayreference.append(Example(animationarrayreferenceX, animationarrayreferenceY))
        animationarrayintermediateY = []
        animationarrayintermediateX = []
        animationarrayreferenceX = []
        animationarrayreferenceY = []
    yArray = np.array(errorarray)
    # return animationarrayfinal;

def animateTraining():
    global element, yArray, line, line2, line3
    yValues = []
    for element in xFinalTrainingArray:
        yValues.append(referencefunction(element))
    yArray = np.array(yValues)
    yValuesNeuralNetwork = []
    for element in xFinalTrainingArray:
        yValuesNeuralNetwork.append(neuralnetwork(element, 0))
    fig = plt.figure()
    # fig1 = plt.figure()
    ax = fig.add_subplot(2, 2, 1)
    ax1 = fig.add_subplot(2, 2, 2)
    ax2 = fig.add_subplot(2, 2, 4)
    # ax3 = fig1.add_subplot(1, 2, 1)
    # ax3 = fig.add_subplot(2, 2, 4)
    # ax1 = fig.add_subplot(2, 2, 2)
    # xValues = np.arange(0, 60, 1)
    line, = ax.plot(animationarrayfinal[0].x, animationarrayfinal[0].y)
    line1, = ax.plot(animationarrayreference[0].x, animationarrayreference[0].y, )
    line2 = ax1.quiver(0, 0, animationweightvectorw1[0][0], animationweightvectorw1[0][1], color='r', angles='xy',
                       scale_units='xy', scale=1)
    line3 = ax2.quiver(0, 0, animationweightvectorw0[0][0], animationweightvectorw0[0][1], color='r', angles='xy',
                       scale_units='xy', scale=1)
    ax.set_title("Neural Network")
    ax.grid()
    ax1.set_title("Weightvectors")
    ax1.grid()
    # ax2.set_title("\n Weightvector Layer 1")
    ax2.grid()
    # line2, = ax.plot(plt.Arrow(1,1,1,1))
    # line, = ax.plot()
    ax.set_ylim(-3, 3)

    # DO NOT DELETE high training weights
    # ax1.set_ylim(-40, 40)
    # ax1.set_ylim(-40, 40)
    # ax1.set_xlim(-40, 40)
    # ax2.set_xlim(-40, 1000)
    # ax2.set_ylim(-40, 1000)

    # DO NOT DELETE small trainingweights
    ax1.set_ylim(-10, 10)
    # ax1.set_ylim(-10, 10)
    ax1.set_xlim(-10,10)
    ax2.set_xlim(-10,10)
    ax2.set_ylim(-10,10)
    # ax1.set_ylim(0, 2.5)
    # ax1.set_xlim(0, 2.5)
    # ax1.xaxis.set_ticks(np.arange(0,2.5,0.1))
    # ax1.yaxis.set_ticks(np.arange(0,2.5,0.1))
    # # ax1.set_ylim(0, 2.5)
    #
    #
    # ax2.set_xlim(0, 2.5)
    # ax2.xaxis.set_ticks(np.arange(0,2.5,0.5))
    # ax2.set_ylim(0, 2.5)
    # ax2.yaxis.set_ticks(np.arange(0,2.5,0.5))
    ax1.set_yticklabels([])
    ax2.set_yticklabels([])
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ani = animation.FuncAnimation(fig, update, interval=50)
    # plt.grid()
    plt.show()


def startNeuralNetwork():
    prepareTrainingValues()
    initializeweightandbias()
    initialAnimationArray()
    init()
    trainNetwork()
    # animateTraining()
    return animationarrayfinal, animationarrayreference, animationweightvectorfrontendw0, animationweightvectorfrontendw1;


if __name__ == "__main__":
    startNeuralNetwork()
# else:
#     startNeuralNetwork();
# startNeuralNetwork();