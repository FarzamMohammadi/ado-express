export function snakeToCamel(str: string): string {
    return str.replace(/(_\w)/g, match => match[1].toUpperCase());
}