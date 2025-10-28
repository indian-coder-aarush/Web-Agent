import react, {useState, useEffect} from 'react';
import {io} from 'socket.io-client';

const socket = io('http://localhost:1235');

function App() {

    const [messages, setMessages] = useState([]);

    useEffect(() => {
        socket.on("Message", (message) => {
            setMessages((prev) => [...prev, message]);
        })
        socket.on("reading file", (data) => {
            let message = 'Reading File: ';
            console.log(data);
            message += data.content + '\n';
            message += "Reason: " + data.reason + "\n";
            message = {Role: "Agent", Message: message};
            setMessages((prev) => [...prev, message]);
        });
        socket.on("writing file", (data) => {
            console.log(data);
            let message = 'Changing File: ' + data.File + '\n';
            message += "Code Changed:" + data.content + '\n';
            message += "Reason: " + data.reason + "\n";
            message = {Role: "Agent", Message: message};
            setMessages((prev) => [...prev, message]);
        });
        socket.on("running command", (data) => {
            console.log(data);
            let message = 'Running Command: ' + data.content + '\n';
            message += "Reason: " + data.reason + "\n";
            message = {Role: "Agent", Message: message};
            setMessages((prev) => [...prev, message]);
        });
    },[]);

    const [Prompt,setPrompt] = useState('');

    function prompt_change(e){
        setPrompt(e.target.value);
    }

    async function send_prompt(){
        await fetch("http://127.0.0.1:1235/api/receive-prompt", {
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
