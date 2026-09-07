from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# MEMORY INFORMATION
# -----------------------------
@app.route("/api/memory")
def get_memory():

    memory = psutil.virtual_memory()

    return jsonify({
        "total": round(memory.total / (1024 ** 3), 2),
        "used": round(memory.used / (1024 ** 3), 2),
        "available": round(memory.available / (1024 ** 3), 2),
        "percent": memory.percent
    })


# -----------------------------
# PROCESS INFORMATION
# -----------------------------
@app.route("/api/processes")
def get_processes():

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_percent"]
    ):

        try:
            info = process.info

            memory_mb = process.memory_info().rss / (1024 ** 2)

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "memory": round(memory_mb, 2),
                "percent": round(info["memory_percent"], 2)
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    # Sort processes by memory usage
    processes.sort(
        key=lambda process: process["memory"],
        reverse=True
    )

    # Show top 20 processes
    return jsonify(processes[:20])


# -----------------------------
# MEMORY ALLOCATION
# -----------------------------
@app.route("/api/allocation")
def memory_allocation():

    blocks = []

    block_size = 10

    for i in range(1, 6):

        blocks.append({
            "block": i,
            "size": block_size,
            "status": "Allocated"
        })

    return jsonify({
        "message": "Memory allocation demonstration",
        "blocks": blocks
    })


# -----------------------------
# PAGING
# -----------------------------
@app.route("/api/paging")
def paging():

    pages = []

    for page_number in range(1, 6):

        pages.append({
            "page": page_number,
            "frame": page_number,
            "status": "In Memory"
        })

    return jsonify({
        "message": "Paging demonstration",
        "pages": pages
    })


# -----------------------------
# FIFO PAGE REPLACEMENT
# -----------------------------
@app.route("/api/page-replacement")
def page_replacement():

    reference_string = [1, 2, 3, 1, 4, 5, 2]

    frame_size = 3

    frames = []

    page_faults = 0

    steps = []

    for page in reference_string:

        if page in frames:

            steps.append({
                "page": page,
                "frames": frames.copy(),
                "fault": False
            })

        else:

            page_faults += 1

            if len(frames) < frame_size:

                frames.append(page)

            else:

                frames.pop(0)
                frames.append(page)

            steps.append({
                "page": page,
                "frames": frames.copy(),
                "fault": True
            })

    return jsonify({
        "reference_string": reference_string,
        "final_frames": frames,
        "page_faults": page_faults,
        "steps": steps
    })


# -----------------------------
# VIRTUAL MEMORY INFORMATION
# -----------------------------
@app.route("/api/virtual-memory")
def virtual_memory():

    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return jsonify({
        "ram_total": round(memory.total / (1024 ** 3), 2),
        "ram_used": round(memory.used / (1024 ** 3), 2),
        "swap_total": round(swap.total / (1024 ** 3), 2),
        "swap_used": round(swap.used / (1024 ** 3), 2),
        "swap_percent": swap.percent
    })


# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )