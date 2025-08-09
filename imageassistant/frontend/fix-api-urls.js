const fs = require('fs');
const path = require('path');

// Function to recursively find all .vue files
function findVueFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      findVueFiles(filePath, fileList);
    } else if (file.endsWith('.vue')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Function to update file content
function updateFileContent(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  let updated = false;
  let newContent = content;
  
  // Replace process.env.VUE_APP_API_URL with API_URL
  if (content.includes('process.env.VUE_APP_API_URL')) {
    newContent = newContent.replace(/process\.env\.VUE_APP_API_URL/g, 'API_URL');
    updated = true;
  }
  
  // Add import for API_URL if needed and not already present
  if (updated && !content.includes("import { API_URL }") && !content.includes("from './config.js'")) {
    const scriptMatch = newContent.match(/<script[^>]*>/);
    if (scriptMatch) {
      const scriptIndex = newContent.indexOf(scriptMatch[0]) + scriptMatch[0].length;
      
      // Find existing imports to add our import after them
      const importMatch = newContent.slice(scriptIndex).match(/^[\s\S]*?(import[\s\S]*?from[^\n]*\n)/);
      
      let importInsertIndex;
      let importStatement;
      
      if (filePath.includes('components/auth/') || filePath.includes('components/image/') || filePath.includes('components/payment/') || filePath.includes('components/user/')) {
        importStatement = "import { API_URL } from '../../config.js';\n";
      } else if (filePath.includes('components/')) {
        importStatement = "import { API_URL } from '../config.js';\n";
      } else {
        importStatement = "import { API_URL } from './config.js';\n";
      }
      
      if (importMatch) {
        importInsertIndex = scriptIndex + importMatch[1].length;
      } else {
        importInsertIndex = scriptIndex + 1;
      }
      
      newContent = newContent.slice(0, importInsertIndex) + importStatement + newContent.slice(importInsertIndex);
    }
  }
  
  // Write updated content back to file
  if (updated) {
    fs.writeFileSync(filePath, newContent, 'utf8');
    console.log(`Updated: ${filePath}`);
    return true;
  }
  
  return false;
}

// Main execution
const srcDir = path.join(__dirname, 'src');
const vueFiles = findVueFiles(srcDir);

console.log('Found', vueFiles.length, 'Vue files');

let updatedCount = 0;
vueFiles.forEach(filePath => {
  if (updateFileContent(filePath)) {
    updatedCount++;
  }
});

console.log(`Updated ${updatedCount} files with API_URL configuration`);