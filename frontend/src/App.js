import logo from "./logo.svg";
import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Row, Col } from "react-bootstrap";
function App() {
  const [products, setProducts] = useState([]);
  const [content, setContent] = useState("");
  const [suggestion, setSuggestion] = useState("");
  const [sensitiveWords, setSensitiveWords] = useState("");
  const [label, setLabel] = useState("");
  const [result, setResult] = useState("");
  // const [flag, setFlag] = useState(false);
let flag=false
  const findSensitiveWords = async () => {
    console.log('send flag', flag)
    const { data } = await axios.post(
      `http://127.0.0.1:8000/api/alicloud/`,
      { content: content },
      config
    );
    console.log("data", data);
    let suggestion = data.data[0].results[0].suggestion;
    if (suggestion === "block") {
     // setFlag(true);
      flag=true
      let sensitiveWords = data.data[0].results[0].details[0].hasOwnProperty(
        "contexts"
      )
        ? data.data[0].results[0].details[0].contexts[0].context
        : "";
      let label = data.data[0].results[0].label;
      let wordsResult = sensitiveWords
        ? `您的输入内容有敏感信息\n 敏感信息为：${sensitiveWords}\n 敏感类型：${label}`
        : `您的输入内容有敏感信息\n 敏感类型：${label}`;
      console.log(
        `您的输入内容有敏感信息\n 敏感信息为：${sensitiveWords}\n 敏感类型：${label}`
      );
      setResult(wordsResult + "\n 请去除敏感信息，重新提交");
    } else {
      setSuggestion("");
      setSensitiveWords("");
      setLabel("");
    }
  };

  const makeItBetter = async () => {
    await findSensitiveWords();
    console.log('chinese flag', flag)
    if (!flag) {
      console.log('chinese', content)
      const { data } = await axios.post(
        `http://127.0.0.1:8000/api/betterchinese/`,
        { content: content },
        config
      );
      console.log("good chinese data", data);
      console.log('good chinese result', result)
     
      setResult(data);
    }
    else {
     // setFlag(prv=>!prv);
     flag=false
    }
   
  };
  const translate = async () => {
   await findSensitiveWords();
    console.log('english flag', flag)
    if (!flag) {
      console.log('english', content)
      const { data } = await axios.post(
        `http://127.0.0.1:8000/api/transenglish/`,
        { content: content },
        config
      );
      console.log("translation data", data);
      console.log('trans result', result)
     
      setResult(data);
    }
    else {
     // setFlag(prv=>!prv);
     flag=false
    }
   
  };

  const config = {
    headers: {
      "Content-type": "application/json",
    },
  };
  const handleSubmit = () => {};

  useEffect(() => {
    // async function fetchProducts() {
    //   // const { data } = await axios.get("http://127.0.0.1:8000/api/products/");
    //   // console.log('data', data)
    //   const { data } = await axios.post(
    //     `http://127.0.0.1:8000/api/products/`,
    //     { test: "nice try" },
    //     config
    //   );
    //   setProducts(data);
    // }
    // fetchProducts();
  }, []);
  return (
    <div className="App">
      <h1>Beauty & translate the text</h1>
      <br></br>

      <form onSubmit={handleSubmit}>
        {" "}
        {/* Need an action */}
        <div className="container">
          <textarea
            id="textarea"
            className="textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          ></textarea>
          <div className="button-container">
            <input type="button" value="潤色" onClick={makeItBetter}></input>
            <input type="button" value="翻譯" onClick={translate}></input>
          </div>
          <textarea
            id="textarea"
            className="textarea"
            value={result}
          ></textarea>
        </div>
      </form>
    </div>
  );
}

export default App;
