const fs = require('fs');
const path = require('path');

const answersDir = path.join(__dirname, '../docs/answers');
const outputFile = path.join(__dirname, '../docs/merged-answers.md');

// Read all markdown files from the answers directory
const files = fs.readdirSync(answersDir)
    .filter(file => file.endsWith('.md'))
    .sort(); // Sort files alphabetically

let mergedContent = '# Combined Health Economic Impact Analysis\n\n';

// Process each file
files.forEach(file => {
    const filePath = path.join(answersDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Add a section divider and the original filename as a heading
    mergedContent += `\n---\n\n`;
    mergedContent += `# ${path.basename(file, '.md').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}\n\n`;
    mergedContent += content + '\n';
});

// Write the merged content to the output file
fs.writeFileSync(outputFile, mergedContent);

console.log(`Successfully merged ${files.length} files into ${outputFile}`); 