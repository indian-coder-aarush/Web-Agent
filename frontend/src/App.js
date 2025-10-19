import react, {useState} from 'react';

function App() {
    const [Prompt,setPrompt] = useState('');

    function prompt_change(e){
        setPrompt(e.target.value);
    }

    async function send_prompt(){
        await fetch("http://127.0.0.1:1234///api/receive-prompt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: Prompt })
        });
    }

    function button_click(){
        send_prompt();
        setPrompt('');
    }

    return (
        <div className = "prompt-input-container">
            <textarea onChange={prompt_change} value={Prompt} className="prompt-input"/>
            <br />
            <button onClick={button_click} className = "submit-button">↑</button>
        </div>
)
}

export default App;
