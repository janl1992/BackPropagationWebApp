import React, {Component} from 'react';
import CanvasJSReact from '../ExternalDependencies/canvasjs.react.js';
import axios from "axios";
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
var dps = [{x: 1, y: 1}, {x: 2, y: 1}, {x: 3, y: 1}, {x: 4, y: 1}, {x: 5, y: 1}, {x: 6, y: 1}, {x: 7, y: 1}, {
    x: 8,
    y: 1
}, {x: 9, y: 1}, {x: 10, y: 1}, {x: 11, y: 1}, {x: 12, y: 1}, {x: 13, y: 1}, {x: 14, y: 1}, {x: 15, y: 1}, {
    x: 16,
    y: 1
}, {x: 17, y: 1}, {x: 18, y: 1}, {x: 19, y: 1}, {x: 20, y: 1}
    , {x: 21, y: 1}, {x: 22, y: 1}, {x: 23, y: 1}, {x: 24, y: 1}, {x: 25, y: 1}, {x: 26, y: 1}, {x: 27, y: 1}, {
        x: 28,
        y: 1
    }, {x: 29, y: 1}, {x: 30, y: 1}
];   //dataPoints.
var dps2 = [{x: 1, y: 1}, {x: 2, y: 1}, {x: 3, y: 1}, {x: 4, y: 1}, {x: 5, y: 1}, {x: 6, y: 1}, {x: 7, y: 1}, {
    x: 8,
    y: 1
}, {x: 9, y: 1}, {x: 10, y: 1}, {x: 11, y: 1}, {x: 12, y: 1}, {x: 13, y: 1}, {x: 14, y: 1}, {x: 15, y: 1}, {
    x: 16,
    y: 1
}, {x: 17, y: 1}, {x: 18, y: 1}, {x: 19, y: 1}, {x: 20, y: 1}
    , {x: 21, y: 1}, {x: 22, y: 1}, {x: 23, y: 1}, {x: 24, y: 1}, {x: 25, y: 1}, {x: 26, y: 1}, {x: 27, y: 1}, {
        x: 28,
        y: 1
    }, {x: 29, y: 1}, {x: 30, y: 1}
];
var updateInterval = 1000;
var counter = 0;
var startingCounter = 0;
var intermediateArray = [];
var intermediateReferenceArray = [];

class FormularComponentAsClass extends Component {

    constructor() {
        super();
        this.updateChart = this.updateChart.bind(this);
        this.sendGetRequest = this.sendGetRequest.bind(this);
        this.state = {
            buttonwasclicked: false
        };
    }

    componentDidMount() {
        setInterval(this.updateChart, updateInterval);
    }

    updateChart() {
        console.log("updatechart was called");
        if (this.chart) {
            if (intermediateArray.length > 0) {
                counter = counter + 30;
                dps = intermediateArray.slice(startingCounter, counter);
                dps.map((item, index) => {
                    this.chart.options.data[0].dataPoints[index].x = item.x;
                    this.chart.options.data[0].dataPoints[index].y = item.y
                });
                if (intermediateReferenceArray.length > 0) {
                    intermediateReferenceArray.map((item, index) => {
                        this.chart.options.data[1].dataPoints[index].x = item.x;
                        this.chart.options.data[1].dataPoints[index].y = item.y;
                    });
                }
                startingCounter = counter;
            }

            this.chart.render();
        }
    }

    sendGetRequest() {
        axios.get('/multilayerperceptron').then(response => {
            console.log("response is:", response);
            response.data.map((item) => {
                item.x.map((itemchildx, index) => {
                    intermediateArray.push({x: itemchildx, y: item.y[index]})
                })
            });
            this.setState(() => ({buttonwasclicked: true}));
        });
        axios.get('/getreference').then(response => {
            console.log("Referenceresponse is:", response);
            response.data.x.map((item, index) => {
                intermediateReferenceArray.push({x: item, y: response.data.y[index]})
            })
        });
    }

    render() {
        const options = {
            title: {
                text: "Neural Network"
            },
            data: [{
                type: "line",
                dataPoints: dps
            },
                {
                    type: "line",
                    dataPoints: dps2
                }
            ]
        };
        return (
            <React.Fragment>
                {this.state.buttonwasclicked ? <div className="justify-content-center mt-5">
                    <button disabled type="button" className="btn btn-primary btn-lg"
                            onClick={e => this.sendGetRequest()}>Start
                        Neural
                        Network
                    </button>
                </div> : <div className="justify-content-center mt-5">
                    <button type="button" className="btn btn-primary btn-lg" onClick={e => this.sendGetRequest()}>Start
                        Neural
                        Network
                    </button>
                </div>}
                {this.state.buttonwasclicked && (dps.length !== 0 ?
                    <div>
                        <CanvasJSChart options={options}
                                       onRef={ref => this.chart = ref}
                        />
                        {/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
                    </div> : <div>Loading</div>)}
            </React.Fragment>
        );
    }
}

export default FormularComponentAsClass;