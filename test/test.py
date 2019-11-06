import json
from sdk.content_recogniser_sdk import ContentRecogniserSDK


def main():
	sdk = ContentRecogniserSDK('aleksas', 'ginkluote69')
	result = sdk.recognise_from_directory('./test_files')
	with open('result.json', 'w') as res_file:
		res_file.write(json.dumps(result, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
	main()
