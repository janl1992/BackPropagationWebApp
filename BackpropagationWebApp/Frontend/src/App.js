import React, { Component } from 'react';
// import FormularComponent  from './component/FormularComponent';
import FormularComponentAsClass  from './component/FormularComponentAsClass';
// import Testcomponent from './component/Testcomponent';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <FormularComponentAsClass />
        {/*<Testcomponent />*/}
      </div>
    );
  }
}

export default App;
