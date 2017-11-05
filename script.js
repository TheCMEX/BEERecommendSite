const App = () => {
    return [<HeelpClass/>]
}

class HeelpClass extends React.Component{
    increment(){
    this.setState((prev_state) => {
        return {counter: prev_state.counter+1}
    })
}
    constructor(props){
        super(props);
        this.state={
            counter: 0,
        }
    }
    render(){
        return (
        <h1>
            {this.state.counter}
            <button onClick={() => this.increment()}>ДААААААА</button>
        </h1>)
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);