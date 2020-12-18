from bs4 import BeautifulSoup
import requests
import re

pages = ["https://pytorch.org/docs/stable/torch.html",
         "https://pytorch.org/docs/stable/nn.html",
         "https://pytorch.org/docs/stable/nn.functional.html",
         "https://pytorch.org/docs/stable/tensors.html",
         "https://pytorch.org/docs/stable/tensor_attributes.html",
         "https://pytorch.org/docs/stable/tensor_view.html",
         "https://pytorch.org/docs/stable/autograd.html",
         "https://pytorch.org/docs/stable/cuda.html",
         "https://pytorch.org/docs/stable/amp.html",
         "https://pytorch.org/docs/stable/backends.html",
         "https://pytorch.org/docs/stable/distributed.html",
         "https://pytorch.org/docs/stable/distributions.html",
         "https://pytorch.org/docs/stable/fft.html",
         "https://pytorch.org/docs/stable/futures.html",
         "https://pytorch.org/docs/stable/hub.html",
         "https://pytorch.org/docs/stable/jit.html",
         "https://pytorch.org/docs/stable/linalg.html",
         "https://pytorch.org/docs/stable/nn.init.html",
         "https://pytorch.org/docs/stable/onnx.html",
         "https://pytorch.org/docs/stable/optim.html",
         "https://pytorch.org/docs/stable/complex_numbers.html",
         "https://pytorch.org/docs/stable/quantization.html",
         "https://pytorch.org/docs/stable/rpc.html",
         "https://pytorch.org/docs/stable/random.html",
         "https://pytorch.org/docs/stable/sparse.html",
         "https://pytorch.org/docs/stable/storage.html",
         "https://pytorch.org/docs/stable/bottleneck.html",
         "https://pytorch.org/docs/stable/checkpoint.html",
         "https://pytorch.org/docs/stable/cpp_extension.html",
         "https://pytorch.org/docs/stable/data.html",
         "https://pytorch.org/docs/stable/dlpack.html",
         "https://pytorch.org/docs/stable/mobile_optimizer.html",
         "https://pytorch.org/docs/stable/model_zoo.html",
         "https://pytorch.org/docs/stable/tensorboard.html",
         "https://pytorch.org/docs/stable/type_info.html",
         "https://pytorch.org/docs/stable/named_tensor.html",
         "https://pytorch.org/docs/stable/name_inference.html",
         "https://pytorch.org/docs/stable/__config__.html"]

f = open("torch_apis.txt", "w", encoding = "utf-8")
for page in pages:
    page_contents = requests.get(page)
    soup = BeautifulSoup(page_contents.content, 'html.parser')
    result = soup.find_all(name = "tr", attrs = {"class":["row-odd", "row-even"]})

    # print(str(result[0]))
    # print(p.search(str(result[0])))

    # match = p.search(str(result[0]))
    # print(match.group(0))

    for line in result:
        m = re.search(r'id="[\w.]+"|title="[\w.]+"', str(line))
        if m:
            m = m.group(0)
            m = m.split("\"")[1]
            f.write(m + "\n")

    f.write("---------\n")
f.close()


#print(*result, sep = "\n")
# print(*matches, sep = "\n")