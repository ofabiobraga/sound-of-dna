import React from "react";

const Panel = ({ title, description, files }) => {
    return (
        <div>
            <h2>{title}</h2>
            <p>{description}</p>
            <Dropdown />
            <ul>
                {files.map((file, index) => (
                    <li key={index}>
                        <audio controls>
                            <source src={file.mp3} type="audio/mpeg" />
                        </audio>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Panel;
