import os
import subprocess
import time
import hashlib
import uuid
from pathlib import Path
from app.services.mork_generator import MorkQueryGenerator
from hyperon import MeTTa
import logging

logger = logging.getLogger(__name__)
class MorkCLIQueryGenerator(MorkQueryGenerator):
    def __init__(self, dataset_path):
        super().__init__(dataset_path=None)
        self.dataset_path = Path(dataset_path)
        project_root = Path(__file__).resolve().parents[2]
        default_wrapper = project_root / "scripts" / "mork_docker_wrapper.py"
        if default_wrapper.exists():
            self.mork_bin = str(default_wrapper)
        else:
            raise RuntimeError("MORK docker wrapper not found.")
        self.metta = MeTTa()

    def is_ready(self):
        act_file = self.dataset_path / "annotation.act"
        return act_file.exists()

    def connect(self):
        return None
        
    def run_query(self, query, stop_event=None, species='human'):   
        pattern_tuple, template_tuple, query_type = query
        
        pattern_str = " ".join(pattern_tuple)
        template_str = " ".join(template_tuple)

        dataset_id = hashlib.md5(str(self.dataset_path.resolve()).encode()).hexdigest()[:8]
        target_space = f"mork_{dataset_id}"
        
        act_file = self.dataset_path / "annotation.act"
        shm_act = Path("/dev/shm") / f"{target_space}.act"

        if not act_file.exists():
            message = (
                f"Missing ACT file: {act_file}. "
                "Run 'python scripts/build_act.py' to generate it."
            )
            logger.error(message)
            raise FileNotFoundError(message)
        
        if not shm_act.exists() or (act_file.stat().st_mtime > shm_act.stat().st_mtime):
            try:
                temp_shm = Path("/dev/shm") / f"{shm_act.name}.tmp.{uuid.uuid4().hex}"
                os.symlink(act_file.resolve(), temp_shm)
                os.replace(temp_shm, shm_act)
            except Exception as e:
                if not shm_act.exists():
                    logger.error(f"SHM Symlink update failed: {e}")
        
        if len(pattern_tuple) == 1:
            act_pattern = pattern_tuple[0]
            template_body = template_str
        else:
            act_pattern = f'(, {pattern_str})'
            template_body = template_str
        
        metta_query = f'(exec 0 (I (ACT {target_space} {act_pattern})) (, {template_body}))'
        
        query_id = uuid.uuid4().hex
        query_file_name = f"query_{query_id}.metta"
        query_file = self.dataset_path / query_file_name
        
        try:
            with open(query_file, "w") as f:
                f.write(metta_query)
            

            run_cmd = [self.mork_bin, "run", query_file_name]
            try:
                result = subprocess.run(run_cmd, capture_output=True, text=True, check=True, cwd=str(self.dataset_path))
                raw_output = result.stdout
            except subprocess.CalledProcessError as e:
                app.logger.error(f"MORK CLI Error Executing {run_cmd}: {e.stderr}")
                return [[]]

            if "result:" in raw_output:
                actual_result = raw_output.split("result:", 1)[1].strip()
            else:
                actual_result = raw_output.strip()

            metta_result = self.metta.parse_all(actual_result)
            
            return [metta_result]
        finally:
            if query_file.exists():
                try:
                    query_file.unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete temp query file {query_file}: {e}")
