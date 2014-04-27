<?php

	$options = getopt("p:");

	if (count($options) != 1)
		exit ("Please specify path (-p).");
	
	$path = $options['p'];
	
	if (! file_exists($path) ) 
		exit ("Invalid path name.");

	set_include_path(get_include_path() . PATH_SEPARATOR . $path);
	
	$dirItr = new RecursiveDirectoryIterator($path, RecursiveDirectoryIterator::SKIP_DOTS);
	
	$filter = new RecursiveCallbackFilterIterator($dirItr, function ($current, $key, $iterator) {
		if ($current->isDir())
			return $current->getFilename()[0] != '.';
		else 
			return $current->getExtension() === 'php';
		});


	$objects = new RecursiveIteratorIterator($filter, RecursiveIteratorIterator::SELF_FIRST);

	foreach($objects as $name => $d)
	{
		if (strpos($d->getFilename(), '.php') !== FALSE) 
		{
			$file_path = $d->getPath() . DIRECTORY_SEPARATOR . $d->getFilename();
			hash_functions($file_path);
		}		
	}
	
	function hash_functions($file_path)
	{
		$content = file_get_contents($file_path);
		$tokens = token_get_all($content);
		$functions = array();
		
		$class_name = null;
		$function_name = null;
		$function_body = null;
		
		$count = count($tokens);
		$brace_count = 0;
		for ($i = 2; $i < $count; $i++) 
		{
			if ($tokens[$i - 2][0] == T_CLASS && $tokens[$i - 1][0] == T_WHITESPACE && $tokens[$i][0] == T_STRING)
				$class_name = $tokens[$i][1];
			if ($tokens[$i - 2][0] == T_FUNCTION && $tokens[$i - 1][0] == T_WHITESPACE && $tokens[$i][0] == T_STRING) 
				$function_name = $class_name.'::'.$tokens[$i][1];
			else if ($function_name != null)
			{	
				if (is_array($tokens[$i]))
					$function_body  .= $tokens[$i][1];
				else
					$function_body  .=  $tokens[$i];

				if($tokens[$i] == '{')
					$brace_count = $brace_count + 1;
				else if ($tokens[$i] == '}')
				{
					$brace_count = $brace_count - 1;
					if ($brace_count == 0)
					{
						output_functions($function_name, $function_body);
						$function_name = null;
						$function_body = null;
					}
				}				
			}
		}
	}
	
	function output_functions($function_name, $function_body)
	{
		//remove whitespaces
		$function_body = preg_replace('!\s+!', '', $function_body);
		//echo $function_body.PHP_EOL;
		$hash = hash ("adler32", $function_body);
		echo $function_name.' '.$hash.PHP_EOL;
	}	
?>
