import './App.css';
import react, {useState} from 'react';

function App() {
    const [Prompt,setPrompt] = useState('');
    function prompt_change(e){
        setPrompt(e.target.value);
    }
    return (
        <>
            <input onChange={prompt_change} value={Prompt}/>
        </>
    )
}

export default App;
