import react, {useState} from 'react';

function App() {
    const [Prompt,setPrompt] = useState('');

    function prompt_change(e){
        setPrompt(e.target.value);
    }

    function button_click(){
        setPrompt('');
    }

    return (
        <div className = "prompt-input-container">
            <input onChange={prompt_change} value={Prompt} className="prompt-input"/>
            <br />
            <button onClick={button_click} className = "submit-button">↑</button>
        </div>
)
}

export default App;
