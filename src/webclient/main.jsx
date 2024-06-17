import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

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
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(App));
