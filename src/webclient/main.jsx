import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
    const [clicked, setClicked] = useState(false);

    function MyButton() {
        return <button onClick={()=>setClicked(!clicked)}>Button</button>;
    }
    return (
        <div>
            <p>
                <MyButton />
            </p>
            <p>This button has been {clicked ? 'clicked' : 'unclicked'}</p>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(App));
