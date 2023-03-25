
export class Endpoints {
    static baseUrl = 'http://127.0.0.1:8000';

    // Search
    static searchViaEnvironment = `${this.baseUrl}/search/via-environment`;
    static searchViaLatest = `${this.baseUrl}/search/via-latest`;
    static searchViaNumber = `${this.baseUrl}/search/via-number`;
    static searchViaQuery = `${this.baseUrl}/search/via-query`;

    //Deploy
    static deploy = `${this.baseUrl}/deploy`;
}

