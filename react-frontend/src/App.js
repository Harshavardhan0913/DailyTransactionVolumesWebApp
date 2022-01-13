import './App.css';
import React, {useState, useEffect} from "react";
import * as ReactBootStrap from 'react-bootstrap'
import ReactLoading from 'react-loading';

function App() {

    const [data, setData] = useState([])
    const [loading, setLoading] = useState(true)

  useEffect(() =>{
    fetch("/get_data").then(
        res => res.json()
    ).then(
        data => {
            setData(data)
            setLoading(false)
          console.log(data)
        }
    )
  },[])

  return (
    <div>
        <div className='App-header'>
            <div><img src="/unilend.svg"/></div><div>UBoost Daily Transaction Volumes</div> </div>
        <br/>
        {(loading)?(
            <ReactLoading className='container' type='bars' color='#4169E1' height={80} width={80} />
        ):(
            <div class="container"  >
                <ReactBootStrap.Table striped bordered hover variant='dark'>
                    <thead>
                        <tr>
                            <th>Contract Name</th>
                            <th>Balance</th>
                            <th>24 Hr Balance Increase</th>
                            <th>Volume</th>
                            <th>24 Hr Vol. Increase</th>
                        </tr>
                    </thead>
                    {data.map((d,i) =>{
                        return (
                        <tbody>
                            <tr key={i}>
                                <td>{d.contract}</td>
                                <td>{d.balance}</td>
                                <td>{d.balance_diff}</td>
                                <td>{d.volume}</td>
                                <td>{d.vol_change}</td>
                            </tr>
                        </tbody>
                            )
                        })
                    }
                    </ReactBootStrap.Table>
            </div>
        )}

    </div>
  );
}

export default App;
