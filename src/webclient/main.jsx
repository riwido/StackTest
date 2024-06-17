import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';

function WebSocketComponent() {
    const [message, setMessage] = useState('');
    useEffect(() => {
        const socket = new WebSocket('ws');

        socket.onopen = () => {
            console.log('Websocket connected');
        };

        socket.onmessage = (event) => {
            console.log(JSON.stringify(event));
            setMessage(event.data);
        };
        return () => socket.close();
    }, []);
    return (
        <div>
            <p>The server says: {JSON.stringify(message)}</p>
        </div>
    );
}

function App() {
    const [clicked, setClicked] = useState(false);
    const [data, setData] = useState('');

    function fetchData() {
        fetch('data').then((response) =>
            response.json().then((data) => setData(data.data)),
        );
    }
    function MyButton() {
        return <button onClick={() => setClicked(!clicked)}>Button</button>;
    }
    function DataRetrieve() {
        return <button onClick={() => fetchData()}>Retrieve Data</button>;
    }
    return (
        <div>
            <p>
                <MyButton />
            </p>
            <p>This button has been {clicked ? 'clicked' : 'unclicked'}</p>
            <DataRetrieve />
            <p>Data: {data}</p>
            <WebSocketComponent />
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(App));
