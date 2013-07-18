from setuptools import setup, find_packages
	
setup(
		name='mp3fm',
		version='1.0.1',
		author='Akshit Agarwal',
		author_email='akshit.jiit@gmail.com',
		url='https://github.com/Aki92/mp3fm',
		packages=find_packages(),
		entry_points = {
			'console_scripts': ['mp3fm = mp3fm.mp3fm:main']
						}, 
		install_requires=['mutagen', 'musicbrainzngs'], 
		license='MIT', 
		description='''Packs the Songs into folders corresponding to its \
		properties like Album(Movie)/Artist/Year/Comments/Title/Duration''', 
		long_description=open('README.md').read(), 
		classifiers=["Environment :: Console"],
			
	)
		