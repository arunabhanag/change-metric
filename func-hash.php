<?php

	$options = getopt("p:");

	if (count($options) != 1)
		exit ("Please specify path (-p).");
	
	$path = $options['p'];
	
	//echo "processing files from " . $path . PHP_EOL;
	
	if (! file_exists($path) ) 
		exit ("Invalid path name.");

	$dirItr = new RecursiveDirectoryIterator($path, RecursiveDirectoryIterator::SKIP_DOTS);
	
	$filter = new RecursiveCallbackFilterIterator($dirItr, function ($current, $key, $iterator) {
		if ($current->isDir())
			return $current->getFilename()[0] != '.';
		else 
			return $current->getExtension() === 'php';
		});


	$objects = new RecursiveIteratorIterator($filter, RecursiveIteratorIterator::SELF_FIRST);

	foreach($objects as $name => $d){
		if (strpos($d->getFilename(), '.php') !== FALSE) 
		{
				echo $d->getPath() . DIRECTORY_SEPARATOR . $d->getFilename() . PHP_EOL;
		}
	}
	
?>
