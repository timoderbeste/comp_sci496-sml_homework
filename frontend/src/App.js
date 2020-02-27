import React, {useEffect, useState} from 'react';
import 'rbx/index.css';
import {Container, Button, Title, File, Input, Image, List, Column} from 'rbx';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faUpload} from '@fortawesome/free-solid-svg-icons';


const get_image_idxes_url = '/img_ids_with_img';
const get_image_with_idx_url = '/image';

const App = () => {

  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadedImageURL, setUploadedImageURL] = useState(null);
  const [modificationText, setModificationText] = useState(null);
  const [retrievedIdxes, setRetrievedIdxes] = useState([]);
  const [retrievedImages, setRetrievedImages] = useState([]);

  const getBase64 = (file, cb) => {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        cb(reader.result);
    };
    reader.onerror = function (error) {
        console.log('Error: ', error);
    };
}

  const fileChangedHandler = (event) => {
    console.log('fileChangedHandler called');
    const file = event.target.files[0];
    console.log(file);
    setUploadedImage(file);
    setUploadedImageURL(URL.createObjectURL(file));
  }


  const modChangedHandler = (event) => {
    console.log(event.target.value);
    setModificationText(event.target.value);
  }

  const getImagesWithIdxes = async (imageIdxes) => {
    const imageBase64s = [];
    for (let i = 0; i < imageIdxes.length; i++) {
      const queryData = {
        'img_id': imageIdxes[i],
      };
      const response = await fetch(get_image_with_idx_url, {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(queryData)
      });
      const data = await response.json();
      imageBase64s.push(data['img_base64']);
    }

    setRetrievedImages(imageBase64s);
  };

  const submitQuery = (event) => {
    console.log('Submitting Query');
    console.log(modificationText);
    console.log(uploadedImage);
    getBase64(uploadedImage, (imgBase64) => {
      console.log(imgBase64);
      const queryData = {
        'img_base64': imgBase64,
        'mod': modificationText
      };

      fetch(get_image_idxes_url, {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(queryData)
      }).then((response) => {
        if (response.ok) {
          response.json().then(data => {
            console.log(data);
            const imageIdxes = data['img_ids'];
            setRetrievedIdxes(data['img_ids']);
            getImagesWithIdxes(imageIdxes);
          });
        }
      }).catch((error) => {
        console.log(error);
      });

    });
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
      <Image src={uploadedImageURL}  width='30%'/>
      <Input type='text' placeholder='Write down your desired modification' onChange={modChangedHandler} />
      <br/>
      <Button onClick={submitQuery}>Compile and Retrieve</Button>

      <Title size={3}>Retrieved Images</Title>
      <Column.Group multiline>
        {retrievedImages.map(retrievedImage => <Column size='one-third'><Image src={`data:image/png;base64,${retrievedImage}`} width='30%'/></Column>)}
      </Column.Group>
    </Container>
  );
};

export default App;
