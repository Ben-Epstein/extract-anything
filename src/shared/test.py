# import asyncio
# from baml_client.async_client import b
# from baml_client.types import Person
# from tqdm.asyncio import tqdm
from shared.baml_client.types import NDA

NDA.agreement_type

resume_text = """
Vaibhav Gupta
vbv@boundaryml.com

Experience:
- Founder at BoundaryML
- CV Engineer at Google
- CV Engineer at Microsoft

Skills:
- Rust
- C++
"""

# resume = b.ExtractResume(resume_text)
# print(resume.name)

# async def extract_all_resumes(all_resumes: list[str]) -> list[Person]:
#     coros = [b.ExtractResume(all_resumes) for res in all_resumes]
#     resumes = await tqdm.gather(*coros)
#     return resumes

# if __name__ == "__main__":
#     resumes = asyncio.run(extract_all_resumes([resume_text]*20))
#     for resume in resumes:
#         print(resume.name, resume.skills)
