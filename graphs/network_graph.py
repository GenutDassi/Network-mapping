import io
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


def get_emoji_image(emoji, size):
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", size - 5)  # Adjust font size as needed
    draw.text((5, 0), emoji, font=font, fill=(0, 0, 0, 255))
    return img


async def show_graph_network(connections_list):
    img_url = "https://media.gcflearnfree.org/content/55e0730c7dd48174331f5164_01_17_2014" \
              "/whatisacomputer_desktop_computers.jpg"
    graph = nx.DiGraph()
    for connection in connections_list:
        src_mac = connection["src_mac"]
        src_ip = connection["src_ip"]
        src_vendor = connection["src_vendor"]
        dst_mac = connection["dst_mac"]
        dst_ip = connection["dst_ip"]
        dst_vendor = connection["dst_vendor"]
        protocol = connection["protocol"]
        graph.add_node(src_mac, vendor=src_vendor, ip=src_ip, shape="box")
        graph.add_node(dst_mac, vendor=dst_vendor, ip=dst_ip, node_imge=img_url)
        graph.add_edge(src_mac, dst_mac, protocol=protocol)
    pos = nx.spring_layout(graph, seed=42)
    edge_colors = [i for i in range(len(graph.edges()))]
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(graph, pos, node_size=300, node_color="skyblue")
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color=edge_colors,
        edge_cmap=plt.get_cmap("rainbow"),
        width=7.0,
        alpha=0.2,
    )
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels={(u, v): d["protocol"] for u, v, d in graph.edges(data=True)}
    )
    plt.title("Network Graph with Rainbow-Colored Edges")
    plt.axis("off")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()
    return buffer
