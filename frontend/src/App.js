import react, {useState, useEffect} from 'react';

function App() {

    const API_BASE =
        process.env.NODE_ENV === "production"
            ? "https://web-agent-fs1u.onrender.com"
            : "http://127.0.0.1:1235";

    if (!localStorage.getItem("token")) {
        localStorage.setItem("token", crypto.randomUUID());
    }

    const [messages, setMessages] = useState([]);
    const [choice, setChoice] = useState('');
    const [Prompt,setPrompt] = useState('');

    function prompt_change(e){
        setPrompt(e.target.value);
    }

    function react_choice(){
        setChoice('React.js');
    }

    function html_choice(){
        setChoice('HTML, CSS, JacaScript');
    }

    useEffect(() => {
        const source = new EventSource(`${API_BASE}/api/send`);

        source.onmessage = (event) => {
            console.log("Received:", event.data);
            setMessages(prev => [...prev, { Role: "Agent", Message: event.data }]);
        };

        source.onerror = (err) => {
            console.error("EventSource failed:", err);
            source.close();
        };

        return () => {
            source.close();
        };
    }, []);

    async function send_prompt(){
        await fetch(`${API_BASE}/api/receive-prompt`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: Prompt + 'Make the app using ' + choice, user_id: localStorage.getItem("token") })
        });
    }

    function button_click(){
        setMessages(prev => [...prev,{Role:"User", Message:Prompt}]);
        send_prompt();
        setPrompt('');
    }

    return (
        <>
            <button onClick={() => {setPrompt('clear!!!!000');
                                          send_prompt();
                                          setPrompt('');
                                          setMessages([]);}}>
                Clear
            </button>
            <button onClick={()=>window.open('/preview/','_blank')}>
                Preview Website
            </button>
            <div className = 'messages'>
            {messages.map((message) => {return (
                <div className = {message.Role}>{message.Message}</div>
            )})}
            </div>
            <br/>
            <div className = "prompt-input-container">
                <textarea onChange={prompt_change} value={Prompt} className="prompt-input"/>
                <br />
                <button onClick = {react_choice}
                        className = {choice === 'React.js' ? 'choice active' : 'choice' }>
                    React.js
                </button>
                <button onClick = {html_choice}
                        className = {choice === 'HTML, CSS, JacaScript' ? 'choice active' : 'choice' }>
                    HTML, CSS, JavaScript
                </button>
                <button onClick={button_click} className = "submit-button">↑</button>
            </div>
        </>
)
}

export default App;
