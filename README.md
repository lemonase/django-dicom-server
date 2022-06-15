# Django DICOM Server

The goal of this project is to make a user friendly, web-accessible interface around [pynetdicom](https://github.com/pydicom/pynetdicom)
so users can create, setup and run their own DICOM server(s).

This project is a WIP and still in the very early stages of development

## TODO

### Implement `rundicomserver` as Django subcommand

This will essentially:

- Run pynetdicom's "storescp" command in the background, but also accept "C-ECHO" messages
- Log parallel to Django - probably to different files
- Eventually be merged into the Django initialization process
