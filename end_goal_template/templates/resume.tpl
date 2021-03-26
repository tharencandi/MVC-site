<!-- Source code by Chen Kang Yang.  -->
<!DOCTYPE html>
<html lang="en-AU">
  <head>
    <meta charset="UTF-8">
    <!--Prevent site from being indexed-->
    <!-- <meta name="robots" content="noindex"> -->
    <title>About me - John Doe</title>
    <meta name="description" content="A brief introduction about myself.">
    
    <!--Open Graph metadata-->
    <meta property="og:title" content="About me - John Doe">
    <meta property="og:description" content="A brief introduction about myself.">
    <meta property="og:image" content="https://example.com/images/logo.png">
    <meta property="og:type" content="article">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#000000">
    
    <link rel="icon" href="images/favicons/favicon.ico">
    <link rel="stylesheet" href="styles/fonts.css">
    <link rel="stylesheet" href="styles/index.css">


  </head>
  
  <body>
     <div class="flex-container">
    <nav>     
      <div id="home">
        <a href="/" title="Back to home">
          <img id="logo_to_root" src="images/cpu.svg" alt="Logo">
        </a>
      </div>                
    </nav>
    </div>
    


    <div class="flex-container">
      <div id="left_bar">
        <img id="profile_picture" src="images/me.jpg" alt="Image of John Doe">
        <h1 id="my_name">John Doe</h1>
        
        <p>
          <img class="left_bar_icon" src="images/key.svg" alt="Key icon">
          <a href="pgp_pubkey.asc" download="" title="Download PGP Public key">
            PGP Public Key
          </a>
          <br>
          Key Fingerprint: 
          <br> 
          <code>00FF FF00 DEAD BEEF CAFE EFAC FEEB DAED 00FF FF00</code>
        </p>
        <p>
          <img class="left_bar_icon" src="images/mail.svg" alt="Email icon">
          <a href="mailto:John Doe<example@example.com>" title="Send me an email" target="_blank" rel="noopener">
            example@example.com
          </a>
        </p>
        <p>
          <img class="left_bar_icon" src="images/github.svg" alt="GitHub icon">
          <a href="https://github.com/" title="Visit GitHub profile" target="_blank" rel="noopener">
            @johndoe
          </a>
        </p>
        <p>
          <img class="left_bar_icon" src="images/gitlab.svg" alt="GitLab icon">
          <a href="https://gitlab.com/" title="Visit GitLab profile" target="_blank" rel="noopener">
            @johndoe
          </a>
        </p>
        <p>
          <img class="left_bar_icon" src="images/instagram.svg" alt="Instagram icon">
          <a href="https://www.instagram.com/" title="Visit Instagram profile" target="_blank" rel="noopener">
            @johndoe
          </a>
        </p>
        <div id="left_bar_button">
          <a href="./files/resume.pdf" title="Download my Résumé" target="_self" rel="noopener">
            <button type="button">
              <img class="left_bar_icon" src="images/file.svg" alt="File icon">
              Download Résumé
            </button>
          </a>
        </div>
      </div>
      <div id="main">      
        <embed src="./files/resume.pdf" width="900" height="1000"  />
      </div>
    </div>
      
      
    <footer>
      <p>
        ~ Original design by <a href="https://github.com/chen-ky/" title="Chen Kang Yang's GitHub profile" target="_blank" rel="noopener">Chen Kang Yang</a> | All rights reserved | Icons by <a href="https://feathericons.com/" title="Feather website" target="_blank" rel="noopener">Feather</a> ~
      </p>
    </footer>
  </body>
</html>

