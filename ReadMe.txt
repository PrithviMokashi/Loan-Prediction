-IMPORTANT : Before running this project please add your SECRET_KEY in setting.py.

-Run the below command to install all the required dependancies.

	pip install -r requirements.txt

-If outside project directory replace "/path/to/" with your project path and run the command.

	pip install -r /path/to/requirements.txt

-Build the Docker container using Dockerfile and run command 
	
	docker run -p 8000:8000 {Container name}:{Container tag}

	or 

	docker run -p 8000:8000 {Container name}

-If running the Image in Docker Desktop, Map the host port name to 8000 under Optional Settings.