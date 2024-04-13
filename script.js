// Replace with your Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyBgjgA7PYySFSDVuiE4cXnC2OcnkIyjBZc",
    authDomain: "demo1-cb6e8.firebaseapp.com",
    projectId: "demo1-cb6e8",
    storageBucket: "demo1-cb6e8.appspot.com",
    messagingSenderId: "231951503459",
    appId: "1:231951503459:web:8a71fd4435af629d5aa856",
    measurementId: "G-ESJXLYXSVW"
  };
  
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  
  // Google Sign-In
  document.getElementById('googleLogin').addEventListener('click', () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    signInWithPopup(provider);
  });
  
  // Facebook Sign-In (Note: You need to replace YOUR_FACEBOOK_APP_ID)
  document.getElementById('facebookLogin').addEventListener('click', () => {
    const provider = new firebase.auth.FacebookAuthProvider();
    signInWithPopup(provider);
  });
  
  function signInWithPopup(provider) {
    firebase.auth().signInWithPopup(provider)
      .then((result) => {
        console.log(result);
      })
      .catch((error) => {
        console.error(error);
      });
  }
  