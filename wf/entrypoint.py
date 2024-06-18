from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, primers: str, gtf: typing.Optional[str], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], aligner: str, capped: typing.Optional[bool], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], chunk: typing.Optional[int], rq: typing.Optional[float], min_passes: typing.Optional[int], min_snr: typing.Optional[float], min_length: typing.Optional[int], max_length: typing.Optional[int], top_passes: typing.Optional[int], five_prime: typing.Optional[int], splice_junction: typing.Optional[int], three_prime: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('primers', primers),
                *get_flag('gtf', gtf),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('chunk', chunk),
                *get_flag('rq', rq),
                *get_flag('min_passes', min_passes),
                *get_flag('min_snr', min_snr),
                *get_flag('min_length', min_length),
                *get_flag('max_length', max_length),
                *get_flag('top_passes', top_passes),
                *get_flag('aligner', aligner),
                *get_flag('capped', capped),
                *get_flag('five_prime', five_prime),
                *get_flag('splice_junction', splice_junction),
                *get_flag('three_prime', three_prime),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_isoseq", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_isoseq(input: LatchFile, primers: str, gtf: typing.Optional[str], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], aligner: str, capped: typing.Optional[bool], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], chunk: typing.Optional[int] = 40, rq: typing.Optional[float] = 0.9, min_passes: typing.Optional[int] = 3, min_snr: typing.Optional[float] = 2.5, min_length: typing.Optional[int] = 10, max_length: typing.Optional[int] = 50000, top_passes: typing.Optional[int] = 60, five_prime: typing.Optional[int] = 100, splice_junction: typing.Optional[int] = 10, three_prime: typing.Optional[int] = 100) -> None:
    """
    nf-core/isoseq

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, primers=primers, gtf=gtf, outdir=outdir, email=email, multiqc_title=multiqc_title, chunk=chunk, rq=rq, min_passes=min_passes, min_snr=min_snr, min_length=min_length, max_length=max_length, top_passes=top_passes, aligner=aligner, capped=capped, five_prime=five_prime, splice_junction=splice_junction, three_prime=three_prime, genome=genome, fasta=fasta, multiqc_methods_description=multiqc_methods_description)

