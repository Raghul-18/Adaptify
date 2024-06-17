const packages = [
	'micropip',
	'packaging',
	'requests',
	'beautifulsoup4',
	'numpy',
	'pandas',
	'matplotlib',
	'scikit-learn',
	'scipy',
	'regex',
	'seaborn'
];

import { loadPyodide } from 'pyodide';
import { writeFile, readFile, copyFile, readdir, rmdir } from 'fs/promises';

async function downloadPackages() {
	console.log('Setting up pyodide + micropip');
	const pyodide = await loadPyodide({
		packageCacheDir: 'static/pyodide'
	});

	const packageJson = JSON.parse(await readFile('package.json'));
	const pyodideVersion = packageJson.dependencies.pyodide;

	const pyodidePackageJson = JSON.parse(await readFile('static/pyodide/package.json'));
	const pyodidePackageVersion = pyodidePackageJson.version;

	if (pyodideVersion.replace('^', '') !== pyodidePackageVersion) {
		console.log('Pyodide version mismatch, removing static/pyodide directory');
		await rmdir('static/pyodide', { recursive: true });
	}

	await pyodide.loadPackage('micropip');
	const micropip = pyodide.pyimport('micropip');
	console.log('Downloading Pyodide packages:', packages);
	await micropip.install(packages);
	console.log('Pyodide packages downloaded, freezing into lock file');
	const lockFile = await micropip.freeze();
	await writeFile('static/pyodide/pyodide-lock.json', lockFile);
}

async function copyPyodide() {
	console.log('Copying Pyodide files into static directory');
	// Copy all files from node_modules/pyodide to static/pyodide
	for await (const entry of await readdir('node_modules/pyodide')) {
		await copyFile(`node_modules/pyodide/${entry}`, `static/pyodide/${entry}`);
	}
}

await downloadPackages();
await copyPyodide();
