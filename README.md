# Quick dev guide


# Create the icon file

Go to the ``./icon`` dir and run the ``./convert_png_to_icns.sh`` script to convert the original ``icon.png`` file into a ``icon.icns`` icon file.

# Build App automatically

Run the shell script ``./install.sh`` that:

1. Cleans the ``build`` and ``dist`` directories: ``clean.sh`` 
2. builds the App using py2app: ``build_standalone.sh``
3. Adds proper links and change App name: ``finalize.sh``
	


