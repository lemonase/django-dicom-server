# Django DICOM Server

## Background

DICOM (Digital Imaging and Communications in Medicine) is a standard protocol
implemented by medical imaging devices such as Ultrasound Systems, CT Xrays
and more. A DICOM Server (SCP aka Service Class Provider) is software that
implements a set of functionality for receiving, querying or simply responding (echo)
to a DICOM client (SCU aka Service Class User).

For more information - refer to the [DICOM wiki article](https://en.wikipedia.org/wiki/DICOM)

## Goals

The goal of this project is to make a user friendly, web-accessible interface around [pynetdicom](https://github.com/pydicom/pynetdicom)
so users can create, setup and run their own DICOM server(s).

This project is a WIP and still in the very early stages of development

## TODO

### Implement `rundicomserver` as Django subcommand

This will essentially:

- Run pynetdicom's "storescp" command in the background, but also accept "C-ECHO" messages
- Log parallel to Django - probably to different files
- Eventually be merged into the Django initialization process
