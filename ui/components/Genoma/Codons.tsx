'use client'

interface GenomaCodonsProps {
    codons: Array<string>;
}

const colors = {
    TTT: 'bg-rose-800',
    TTC: 'bg-pink-800',
    TTA: 'bg-rose-700',
    TTG: 'bg-sky-500',
    CTT: 'bg-pink-700',
    CTC: 'bg-rose-600',
    CTA: 'bg-pink-600',
    CTG: 'bg-rose-500',
    ATT: 'bg-pink-500',
    ATC: 'bg-rose-400',
    ATA: 'bg-pink-400',
    ATG: 'bg-blue-500',
    GTT: 'bg-rose-300',
    GTC: 'bg-pink-300',
    GTA: 'bg-rose-200',
    GTG: 'bg-sky-400',
    TCT: 'bg-emerald-800',
    TCC: 'bg-teal-800',
    TCA: 'bg-emerald-700',
    TCG: 'bg-teal-700',
    CCT: 'bg-rose-100',
    CCC: 'bg-pink-100',
    CCA: 'bg-rose-50',
    CCG: 'bg-pink-50',
    ACT: 'bg-emerald-600',
    ACC: 'bg-teal-600',
    ACA: 'bg-emerald-500',
    ACG: 'bg-teal-500',
    GCT: 'bg-fuchsia-500',
    GCC: 'bg-fuchsia-400',
    GCA: 'bg-fuchsia-300',
    GCG: 'bg-fuchsia-200',
    TAT: 'bg-emerald-400',
    TAC: 'bg-teal-400',
    TAA: 'bg-zinc-800',
    TAG: 'bg-zinc-700',
    CAT: 'bg-yellow-950',
    CAC: 'bg-yellow-900',
    CAA: 'bg-emerald-300',
    CAG: 'bg-teal-300',
    AAT: 'bg-emerald-200',
    AAC: 'bg-teal-200',
    AAA: 'bg-yellow-800',
    AAG: 'bg-yellow-700',
    GAT: 'bg-lime-600',
    GAC: 'bg-lime-500',
    GAA: 'bg-lime-400',
    GAG: 'bg-lime-300',
    TGT: 'bg-emerald-100',
    TGC: 'bg-teal-100',
    TGA: 'bg-zinc-600',
    TGG: 'bg-orange-100',
    CGT: 'bg-yellow-600',
    CGC: 'bg-yellow-500',
    CGA: 'bg-yellow-400',
    CGG: 'bg-yellow-300',
    AGT: 'bg-emerald-50',
    AGC: 'bg-teal-50',
    AGA: 'bg-yellow-200',
    AGG: 'bg-yellow-100',
    GGT: 'bg-fuchsia-50',
    GGC: 'bg-red-300',
    GGA: 'bg-red-200',
    GGG: 'bg-red-100'
}

function play(string:object) {
    alert(string.pitch)
}

export default function Codons({ codons }: GenomaCodonsProps) {
    return (
        <div className="flex flex-wrap">
            {codons.map((codon, i) => {
                return (
                    <button onClick={() => play({pitch: 'C4'})} key={i} className={`p-3 ${colors[codon]} transition-all border-4 border-transparent hover:border-white hover:cursor-pointer text-center`}>
                        <span className="bg-white/30 text-black font-mono text-xs p-1">{codon}</span>
                    </button>
                )
            })}
        </div>
    )
}
