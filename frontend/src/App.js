import React, {useEffect, useState} from 'react';
import 'rbx/index.css';
import {Container, Button, Title, File, Input, Image} from 'rbx';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faUpload} from '@fortawesome/free-solid-svg-icons';


const App = () => {

  const [uploadedImage, setUploadedImage] = useState(null);
  const [retrievedIdxes, setRetrievedIdxes] = useState([]);
  const [retrievedImages, setRetrievedImages] = useState([]);

  const fileChangedHandler = (event) => {
    console.log('fileChangedHandler called');
    const file = event.target.files[0];
    console.log(file);
    setUploadedImage(URL.createObjectURL(file));
  }


  const modChangedHandler = (event) => {

  }

  return (
    <Container as='div' style={{width: '100%', paddingTop: '20px'}}>
      <Title size={1}>Image Retrieval</Title>
      <File onChange={fileChangedHandler}>
        <File.Label>
          <File.Input name="image" />
          <File.CTA>
            <File.Icon>
              <FontAwesomeIcon icon={faUpload} />
            </File.Icon>
            <File.Label as="span">Choose an Image</File.Label>
          </File.CTA>
        </File.Label>
      </File>
      <Image src={uploadedImage}/>
      <Input type='text' placeholder='Write down the desired modification' onChange={modChangedHandler} />
      <br/>
      <Button>Retrieve</Button>

      <Title size={3}>Retrieved Images</Title>
    </Container>
  );
};

export default App;
