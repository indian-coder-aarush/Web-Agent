import react, {useState, useEffect} from 'react';
import io from 'socket.io-client';

function App() {

    //const socket = io('http://localhost:1234');

    const [messages, setMessages] = useState([]);

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
        setMessages(prev => [...prev,{Role:"User", Message:Prompt}]);
        send_prompt();
        setPrompt('');
    }

    return (
        <>
            {messages.map((message) => {return (
                <div className = {message.Role}>{message.Message}</div>
            )})}
            <div className = "prompt-input-container">
                <textarea onChange={prompt_change} value={Prompt} className="prompt-input"/>
                <br />
                <button onClick={button_click} className = "submit-button">↑</button>
            </div>
        </>
)
}

export default App;
