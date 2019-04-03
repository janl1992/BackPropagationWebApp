import React, {useState, useEffect, Component} from 'react';
import axios from 'axios';
// import CanvasJSReact from 'canvas';
import CanvasJSReact from '../ExternalDependencies/canvasjs.react';
// import { chart } from '../ExternalDependencies/canvasjs.min'

const CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
var dps = [];   //dataPoints.
var xVal = dps.length + 1;
var yVal = 15;
const updateInterval = 100000;

export const FormularComponent = (chart) => {
    const [animationarray, alteranimationarray] = useState();
    const [buttonwasclicked, alterbutton] = useState(false);
    const [animationcontinue, alteranimation] = useState(0);
    var intermediateArray = [];
    var counter = 0;
    var startingCounter = 0;
    var updatecounter = 0;
    useEffect(() => {
        renderchart()
    });
    function renderchart() {
        chart.render()
    }
    // CanvasJS.chart
    function sendGetRequest() {
        alterbutton(true);
        axios.get('/multilayerperceptron').then(response => {
                intermediateArray = [];
                response.data.map((item) => {
                    item.x.map((itemchildx, index) => {
                        intermediateArray.push({x: itemchildx, y: item.y[index]})
                    })
                });
                alteranimationarray(intermediateArray);
                setInterval(updateChart(), 1000);
                console.log("response is:", response)
            }
        )
    }

    const updateChart = () => {
        console.log("Animationarray ", animationarray);
        counter = counter + 30;
        if (animationarray) {
            dps = animationarray.slice(startingCounter, counter);
            startingCounter = counter;
            // counter = counter + 30;
            // chart.options.data[0].dataPoints = dps;
            // chart.render();
        }
        // updatecounter = updatecounter + 1;
        alteranimation(updatecounter);
    };

    const options = {
        title: {
            text: "Dynamic Line Chart"
        },
        data: [{
            type: "line",
            dataPoints: dps
        }]
    };
    return (
        <React.Fragment>
            <div className="container">
                <div className="justify-content-center mt-5">
                    <button type="button" className="btn btn-primary btn-lg" onClick={sendGetRequest}>Start Neural
                        Network
                    </button>
                </div>
                <div>{animationcontinue}</div>
                {buttonwasclicked && (animationarray ? <div>array was loaded</div> : <div>loading</div>)}
                {/*<CanvasJSChart options={options}*/}
                {/*               onRef={ref => this.chart = ref}/>*/}

            </div>
            <div>
                <CanvasJSChart options = {options}
                               ref={ref => chart = ref}
                />
            </div>
        </React.Fragment>
    );
};

// FormularComponent.propTypes = {
//
// };
export default FormularComponent;