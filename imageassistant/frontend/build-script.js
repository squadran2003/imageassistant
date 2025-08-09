const fs = require('fs');
const path = require('path');

// Helper function to copy directory recursively
function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  const files = fs.readdirSync(src);
  
  files.forEach(file => {
    const srcPath = path.join(src, file);
    const destPath = path.join(dest, file);
    
    if (fs.statSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  });
}

// Helper function to move file
function moveFile(src, dest) {
  if (!fs.existsSync(src)) return;
  
  const destDir = path.dirname(dest);
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }
  
  fs.copyFileSync(src, dest);
  console.log(`Moved: ${src} -> ${dest}`);
}

console.log('Post-build: Moving files to Django structure...');

const distDir = path.join(__dirname, 'dist');
const templatesDir = path.join(__dirname, '..', 'templates');
const assetsDir = path.join(__dirname, '..', 'assets');

// Move index.html to templates
const indexSrc = path.join(distDir, 'index.html');
const indexDest = path.join(templatesDir, 'index.html');
moveFile(indexSrc, indexDest);

// Move CSS files to assets/css
const cssSrc = path.join(distDir, 'css');
const cssDest = path.join(assetsDir, 'css');
if (fs.existsSync(cssSrc)) {
  copyDir(cssSrc, cssDest);
  console.log('Copied CSS files to assets/css');
}

// Move JS files to assets/js  
const jsSrc = path.join(distDir, 'js');
const jsDest = path.join(assetsDir, 'js');
if (fs.existsSync(jsSrc)) {
  copyDir(jsSrc, jsDest);
  console.log('Copied JS files to assets/js');
}

// Move other assets (images, fonts, etc.)
const distFiles = fs.readdirSync(distDir);
distFiles.forEach(file => {
  if (file !== 'index.html' && file !== 'css' && file !== 'js') {
    const srcPath = path.join(distDir, file);
    const destPath = path.join(assetsDir, file);
    
    if (fs.statSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      moveFile(srcPath, destPath);
    }
  }
});

console.log('Build complete! Files moved to Django structure.');