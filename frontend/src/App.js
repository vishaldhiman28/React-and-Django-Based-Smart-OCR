import React, { Component } from 'react';
import axios from 'axios';
import './index.css';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';


class App extends Component {

  state = {
    image: '',
    image_url:null,
    data_img: []
  };

  

  requestDataOfImage() {
    var id_m=document.getElementById("processMessage");
    var id_processm=document.getElementById("dataFromImage");
    var id_dateMess=document.getElementById("dateMessage");
    var id_dateInfo=document.getElementById("dateInfo");
    id_m.textContent="..... Wait .... Getting the text from Image";


    axios.get(`http://127.0.0.1:8000/Date_From_Image/`)
      .then(res => {
        const data_img = res.data;
        this.setState({ data_img });
        id_processm.setAttribute('style',"border:2px; border-style:solid; border-color:#FF0000; padding: 1em;")
        id_m.textContent="----Here is the Text From Image----";
        id_processm.textContent=this.state.data_img.imageText;
        id_dateMess.textContent="---Date From Data----"
        id_dateInfo.setAttribute('style',"border:2px; border-style:solid; border-color:#FF0000; padding: 1em;")
        id_dateInfo.textContent=this.state.data_img.dateInfo;

      })

  };

  handleChange = (e) => {
    this.setState({
      [e.target.id]: e.target.value
    })
  };
  showImageName(){

    var p_im_name=document.getElementById("u_image_name");
    p_im_name.textContent=this.state.image.name;

  };


  handleImageChange = (e) => {
    this.setState({
      image: e.target.files[0],
      image_url:URL.createObjectURL(e.target.files[0])
    },() => {
    this.showImageName()
   });
  };


  handleSubmit = (e) => {
    e.preventDefault();
    var id_m=document.getElementById("postMessage");
    var id_uploaded=document.getElementById("uploadedImage");
  
    
    id_m.textContent="/-/- Uploading";

    console.log(this.state);
    let form_data = new FormData();
    form_data.append('image', this.state.image, this.state.image.name);
    let url = 'http://127.0.0.1:8000/Date_From_Image/';
    axios.post(url, form_data, {
      headers: {
        'content-type': 'multipart/form-data'
      }
    })
        .then(res => {
          console.log(res.data);  

        id_m.textContent="Image Uploaded Successfully.";
        
        var img_ele=document.createElement("img");
        img_ele.src=this.state.image_url;
        img_ele.setAttribute("width","400");
        img_ele.setAttribute('height',"500")
        var existingImage=id_uploaded.getElementsByTagName("img")
        if(existingImage.length){
         existingImage[0].parentNode.replaceChild(img_ele,existingImage[0]);
        }
        else{
          
          id_uploaded.appendChild(img_ele);
        }
        var id_processm=document.getElementById("dataFromImage");
        id_processm.textContent=" ";
        var id_dateInfo=document.getElementById("dateInfo");
        id_dateInfo.textContent=" ";

        this.requestDataOfImage();
        })
        .catch(err => console.log(err));
     }

  render() {

    return (
      <div className="App">
        <Container id="image_in"fixed>
          <h1>Smart OCR</h1>
          <h2>-----------</h2>
          <div id="Upload_o=image">
           <p>Select an Image to Upload</p>
           <p>
              <input accept="image/*"  id="contained-button-file" style={{ display: "none" }}  type="file" onChange={(event)=>this.handleImageChange(event)} required/>
              <label htmlFor="contained-button-file">
               <Button variant="contained" color="secondary" component="span" >
                   Upload Image
               </Button>
               <p id="u_image_name"></p>
              </label>
          </p>
          <Button  variant="contained" color="secondary" onClick={(event) => this.handleSubmit(event)}>Sumbit</Button>
          </div>
          <p></p>
          <div id='postMessage'></div>
          <p></p>
         <div id="uploadedImage"></div>
          <h2>---------------------</h2> 
        </Container>
       <Container id="image_out" fixed>
        <div id="processMessage"></div>
        <p></p>

        <div id="dataFromImage"></div>

        <div id="dateMessage"></div>
        <div id="dateInfo"></div>
  
       </Container>

       <h3>--Deveoper--</h3>
       <h2> Vishal Dhiman</h2>
      </div>
        
      
    );
  }
}

export default App;
