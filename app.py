from flask import Flask, request, json, jsonify
import os
import hashlib
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

blockchain_dir = 'blocksss/'
blockCount = len(os.listdir(blockchain_dir ))


def gethash(prev_block):
	with open(blockchain_dir +str(prev_block), 'rb') as f:
		content = f.read()

		return hashlib.md5(content).hexdigest()


@app.route("/block-integrity")
def checkIntegrity():
	blocks = os.listdir(blockchain_dir)

	result = []
	for block in blocks[1:]:
		with open(blockchain_dir + block, 'rb') as f:
			print (f)
			blockContent = json.load(f)
		
		prev_hash = blockContent.get("prev_block").get("hash")
		prev_filename = blockContent.get("prev_block").get("prev_filename")

		actual_hash = gethash(prev_filename)

		if actual_hash == prev_hash:
			res = "chain OK"
		else:
			res = "chain not OK"

		f'{prev_filename, res}'

		result.append({"block_name": prev_filename, "message": res})
	return jsonify(result)

		
			
			

def writeBlock(borower, lender, amount):
	prev_block = "block" + str(blockCount)

	data = {
		"borower": borower,
		"lender": lender,
		"amount": amount,
		"prev_block": {
			"hash": gethash(prev_block),
			"prev_filename": "block" + str(blockCount)
		}
	}

	with open(blockchain_dir + "block" + str(blockCount + 1), 'w') as f:
		json.dump(data, f, indent=4, ensure_ascii=False)
		f.write('\n')	


@app.route("/write", methods=['POST'])
def index():
	borower = request.json['borower']
	lender = request.json['lender']
	amount = request.json['amount']




	writeBlock(borower, lender, amount)

	return {"message": "block succesfully added"}

	


if __name__ == "__main__":
	app.run(debug=True)