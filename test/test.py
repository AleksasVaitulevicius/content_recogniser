from sdk.content_recogniser_sdk import ContentRecogniserSDK


def main():
	sdk = ContentRecogniserSDK('aleksas', 'ginkluote69')
	print(sdk.recognise())


if __name__ == '__main__':
	main()