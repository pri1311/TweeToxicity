import React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

import styles from '../styles/search.module.css';

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      answers: "",
      set: false,
      prediction: ""
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  createData(name, percentage) {
    return { name, percentage };
  }

  handleUploadImage(ev) {
    ev.preventDefault();


    const message = {
      'Positive': 'Hurray! Positive tweet :)',
      'Negative': 'Toxicity Alert! :('
    }

    let data = new FormData();
    data = this.input.value

    fetch(`http://127.0.0.1:5002/predict?query=${encodeURIComponent(data)}` , {
      method: "GET",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Credentials": true,
    })
      .then((response) => response.json())
      .then((data) => {
        const results = data;
        const prediction = data.prediction;
        const probabilties = data.probabilties;
        console.log(results);
        this.setState({ answers: probabilties, set: true, prediction: message[prediction] });
      });

  }

  render() {
    return (
      <form onSubmit={this.handleUploadImage}>
        <div className={styles.wrapper}>
          <input className={styles.fileInput}
            ref={(ref) => {
              this.input = ref;
            }}
            type="text"
          />
        </div>
        <br />
        <div>
          <button type="submit" className={styles.matchCandidates}>Match Candidates!</button>
        </div>
        {this.state.set && (
          <div>
        <h3>{this.state.prediction}</h3>
          <TableContainer component={Paper} style={{backgroundColor: 'rgba(29, 161, 242, 0.1)', fontWeight: 'bolder' }}>
            <Table sx={{ minWidth: 500 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell style={{fontWeight: 'bolder'}}>Model/Classifier</TableCell>
                  <TableCell style={{fontWeight: 'bolder'}} align="right">Percentage</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {this.state.answers.map((row) => (
                  <React.Fragment key={row.name}>
                  <TableRow
                    sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                  >
                    <TableCell style={{fontWeight: 'bolder'}} component="th" scope="row">
                      {row[0]}
                    </TableCell>
                    <TableCell style={{fontWeight: 'bolder'}} align="right">{row[1]}</TableCell>
                  </TableRow>
                  </React.Fragment>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          </div>
        )}
      </form>
    );
  }
}

export default Main;