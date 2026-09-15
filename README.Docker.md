### Building and running the API

The Compose stack starts the FastAPI API and an internal MongoDB instance.
Keep the existing `.env` file in the project root (it is never copied into the
image), then run:

```sh
docker compose up --build
```

The API is available at `http://localhost:8000`; its OpenAPI UI is at
`http://localhost:8000/docs`. MongoDB data persists in the `mongo-data` Docker
volume and uploads are retained in `./uploads`.

To stop the stack, use `docker compose down`. Add `--volumes` only when you
also intend to delete the local MongoDB data.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t college-erp-api .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/college-erp-api`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
