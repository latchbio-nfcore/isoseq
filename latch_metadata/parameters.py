
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'primers': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Fasta file of primers sequences',
    ),
    'gtf': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Genome annotation file',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'chunk': NextflowParameter(
        type=typing.Optional[int],
        default=40,
        section_title='CCS options',
        description='ccs --chunk option, define the number of batches to run in parallel',
    ),
    'rq': NextflowParameter(
        type=typing.Optional[float],
        default=0.9,
        section_title=None,
        description='ccs --rq option, define the minimum read quality for CCS selection',
    ),
    'min_passes': NextflowParameter(
        type=typing.Optional[int],
        default=3,
        section_title=None,
        description='ccs --min-passes option, define the minimum number of passes to select a CCS',
    ),
    'min_snr': NextflowParameter(
        type=typing.Optional[float],
        default=2.5,
        section_title=None,
        description='ccs --min-snr option, minimum SNR of subreads to use for generating CCS',
    ),
    'min_length': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='ccs --min-length option, minimum CCS length for CCS selection',
    ),
    'max_length': NextflowParameter(
        type=typing.Optional[int],
        default=50000,
        section_title=None,
        description='ccs --max-length option, maximum CCS length for CCS selection',
    ),
    'top_passes': NextflowParameter(
        type=typing.Optional[int],
        default=60,
        section_title=None,
        description='ccs --top-passes option, maximum number of passes to use for CCS generation',
    ),
    'aligner': NextflowParameter(
        type=str,
        default=None,
        section_title='Aligner option',
        description='Aligner to use for mapping: minimap2 or ultra',
    ),
    'capped': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='TAMA options',
        description='TAMA collapse: Capped RNA?',
    ),
    'five_prime': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='TAMA collapse: 5 prime wobble threshold',
    ),
    'splice_junction': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='TAMA collapse: Splice junction / exon wobble threshold',
    ),
    'three_prime': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='TAMA collapse: 3 prime wobble threshold',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

