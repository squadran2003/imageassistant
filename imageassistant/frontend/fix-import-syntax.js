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

// Function to fix import syntax
function fixImportSyntax(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  let newContent = content;
  let updated = false;

  // Fix malformed import statements like: import { RouterLink } from 'vue-router'import { API_URL } from './config.js';
  const malformedImportPattern = /import\s+{[^}]+}\s+from\s+['"][^'"]+['"]import\s+{[^}]+}\s+from\s+['"][^'"]+['"];/g;
  if (malformedImportPattern.test(content)) {
    newContent = newContent.replace(malformedImportPattern, (match) => {
      // Split the malformed import into two separate imports
      const parts = match.split('import ');
      if (parts.length === 3) {
        return `import ${parts[1]};\nimport ${parts[2]}`;
      }
      return match;
    });
    updated = true;
  }

  // Fix wrong config.js path
  if (newContent.includes("from './config.js'")) {
    // Determine correct path based on file location
    let correctImportPath;
    
    if (filePath.includes('/components/auth/') || filePath.includes('\\components\\auth\\') ||
        filePath.includes('/components/image/') || filePath.includes('\\components\\image\\') ||
        filePath.includes('/components/payment/') || filePath.includes('\\components\\payment\\') ||
        filePath.includes('/components/user/') || filePath.includes('\\components\\user\\')) {
      correctImportPath = '../../config.js';
    } else if (filePath.includes('/components/') || filePath.includes('\\components\\')) {
      correctImportPath = '../config.js';
    } else {
      correctImportPath = './config.js';
    }
    
    newContent = newContent.replace(/from '\.\/config\.js'/g, `from '${correctImportPath}'`);
    updated = true;
  }

  if (updated) {
    fs.writeFileSync(filePath, newContent, 'utf8');
    console.log(`Fixed imports in: ${filePath}`);
    return true;
  }
  
  return false;
}

// Main execution
const srcDir = path.join(__dirname, 'src');
const vueFiles = findVueFiles(srcDir);

console.log('Fixing import syntax in', vueFiles.length, 'Vue files');

let fixedCount = 0;
vueFiles.forEach(filePath => {
  if (fixImportSyntax(filePath)) {
    fixedCount++;
  }
});

console.log(`Fixed imports in ${fixedCount} files`);