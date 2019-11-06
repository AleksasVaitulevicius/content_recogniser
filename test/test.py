import json
from sdk.content_recogniser_sdk import ContentRecogniserSDK


def main():
	sdk = ContentRecogniserSDK('aleksas', 'ginkluote69')
	result = sdk.recognise_from_directory('./test_files')
	print(json.dumps(result, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
	main()
