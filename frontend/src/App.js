import './App.css';
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
        <>
            <input onChange={prompt_change} value={Prompt}/>
            <button onClick={button_click}>submit</button>
        </>
    )
}

export default App;
