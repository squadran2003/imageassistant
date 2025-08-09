const fs = require('fs');
const path = require('path');

// Files with their specific fixes
const fileFixes = [
  {
    file: 'src/components/auth/SignUp.vue',
    find: "import { RouterLink } from 'vue-routerimport { API_URL } from '../../config.js';\n';",
    replace: "import { RouterLink } from 'vue-router';\nimport { API_URL } from '../../config.js';"
  },
  {
    file: 'src/components/auth/ResetPassword.vue', 
    find: "import RobotChecker from '../RobotChecker.vue';import { API_URL } from '../../config.js';",
    replace: "import RobotChecker from '../RobotChecker.vue';\nimport { API_URL } from '../../config.js';"
  },
  {
    file: 'src/components/image/CreateGrayscale.vue',
    find: "import ImagePolling from './ImagePolling.vue';import { API_URL } from '../../config.js';",
    replace: "import ImagePolling from './ImagePolling.vue';\nimport { API_URL } from '../../config.js';"
  },
  {
    file: 'src/components/image/CreateImage.vue',
    find: "import ImagePolling from './ImagePolling.vue';import { API_URL } from '../../config.js';",
    replace: "import ImagePolling from './ImagePolling.vue';\nimport { API_URL } from '../../config.js';"
  },
  {
    file: 'src/components/image/CreateOutline.vue',
    find: "import ImagePolling from './ImagePolling.vue';import { API_URL } from '../../config.js';",
    replace: "import ImagePolling from './ImagePolling.vue';\nimport { API_URL } from '../../config.js';"
  },
  {
    file: 'src/components/image/RemoveBackground.vue',
    find: "import ImagePolling from './ImagePolling.vue';import { API_URL } from '../../config.js';",
    replace: "import ImagePolling from './ImagePolling.vue';\nimport { API_URL } from '../../config.js';"
  },
  {
    file: 'src/components/image/ImagePolling.vue',
    find: "<script>import { API_URL } from '../../config.js';",
    replace: "<script>\nimport { API_URL } from '../../config.js';"
  }
];

fileFixes.forEach(fix => {
  const filePath = path.join(__dirname, fix.file);
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf8');
    if (content.includes(fix.find)) {
      const newContent = content.replace(fix.find, fix.replace);
      fs.writeFileSync(filePath, newContent, 'utf8');
      console.log(`Fixed: ${fix.file}`);
    }
  }
});

console.log('Import fixes complete');